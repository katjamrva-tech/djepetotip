from flask import Flask, request
import pandas as pd
import random
import requests
from sklearn.ensemble import RandomForestClassifier
from datetime import datetime, timedelta

app = Flask(__name__)

# =========================
# HISTORIJSKI PODACI
# =========================

england = pd.read_csv("england.csv")
spain = pd.read_csv("spain.csv")
germany = pd.read_csv("germany.csv")
italy = pd.read_csv("italy.csv")
turkey = pd.read_csv("turkey.csv")

data = pd.concat([england,spain,germany,italy,turkey])

data["goal_diff"] = data["FTHG"] - data["FTAG"]

X = data[["FTHG","FTAG","goal_diff"]]
y = (data["FTHG"] > data["FTAG"]).astype(int)

# =========================
# AI MODEL
# =========================

model = RandomForestClassifier(
    n_estimators=300,
    max_depth=10,
    random_state=42
)

model.fit(X,y)

# =========================
# TOP LIGE
# =========================

leagues = [
"eng.1",
"esp.1",
"ger.1",
"ita.1",
"fra.1",
"eng.2",
"por.1",
"ned.1",
"tur.1",
"bel.1"
]

# =========================
# LOGO TIMOVA
# =========================

def team_logo(team):

    name = team.lower().replace(" ","")

    return f"https://logo.clearbit.com/{name}.com"

# =========================
# UTAKMICE
# =========================

def get_matches():

    matches=[]

    today=datetime.utcnow().date()
    tomorrow=today+timedelta(days=1)

    for league in leagues:

        url=f"https://site.api.espn.com/apis/site/v2/sports/soccer/{league}/scoreboard"

        r=requests.get(url)
        data_api=r.json()

        if "events" not in data_api:
            continue

        for game in data_api["events"]:

            date_str=game["date"]
            match_date=datetime.fromisoformat(date_str.replace("Z","+00:00")).date()

            if match_date!=today and match_date!=tomorrow:
                continue

            home=game["competitions"][0]["competitors"][0]["team"]["displayName"]
            away=game["competitions"][0]["competitors"][1]["team"]["displayName"]

            hg=random.randint(0,3)
            ag=random.randint(0,3)

            diff=hg-ag

            prob=model.predict_proba([[hg,ag,diff]])[0][1]
            percent=int(prob*100)

            if percent>75:
                tip="HOME WIN"
            elif percent>65:
                tip="OVER 2.5"
            else:
                tip="BTTS"

            matches.append({
                "home":home,
                "away":away,
                "chance":percent,
                "tip":tip
            })

    return matches

# =========================
# WEB STRANICA
# =========================

@app.route("/",methods=["GET","POST"])
def home():

    matches=get_matches()

    search_result=""

    if request.method=="POST":

        team=request.form.get("team")

        for m in matches:

            if team.lower() in m["home"].lower() or team.lower() in m["away"].lower():

                search_result=f"""
                <div class='card'>
                <img src='{team_logo(m["home"])}' width='25'>
                {m['home']} vs
                <img src='{team_logo(m["away"])}' width='25'>
                {m['away']} <br>
                AI šansa {m['chance']}% <br>
                Tip: {m['tip']}
                </div>
                """

    ticket=random.sample(matches,min(5,len(matches)))

    tip_dana=max(matches,key=lambda x:x["chance"]) if matches else None

    html="""

<html>

<head>

<title>DjepetoTip</title>

<style>

body{
background:#0f172a;
color:white;
font-family:Arial;
padding:40px
}

.card{
background:#1e293b;
padding:20px;
margin:15px;
border-radius:12px;
width:360px
}

input{
padding:10px;
border:none;
border-radius:6px
}

button{
background:#dc2626;
border:none;
padding:12px 20px;
border-radius:8px;
color:white;
font-size:16px
}

</style>

</head>

<body>

<h1 style="display:flex;align-items:center;gap:10px">

<img src="https://cdn-icons-png.flaticon.com/512/53/53283.png" width="40">

DjepetoTip

</h1>

<form method="POST">

<input name="team" placeholder="Upiši tim (npr Chelsea)">

<button>Pretraži</button>

</form>

<form method="GET">

<button>🎲 Generiši novi tiket</button>

</form>

"""

    html+=search_result

    html+="<h2>🔥 Tip dana</h2>"

    if tip_dana:

        html+=f"""
        <div class='card'>
        {tip_dana['home']} vs {tip_dana['away']} <br>
        AI šansa {tip_dana['chance']}% <br>
        Tip: {tip_dana['tip']}
        </div>
        """

    html+="<h2>💰 AI tiket</h2>"

    for t in ticket:

        html+=f"""
        <div class='card'>
        {t['home']} vs {t['away']} <br>
        AI šansa {t['chance']}% <br>
        Tip: {t['tip']}
        </div>
        """

    html+="<h2>📅 Današnje i sutrašnje utakmice</h2>"

    for m in matches:

        html+=f"""
        <div class='card'>
        <img src='{team_logo(m["home"])}' width='25'>
        {m['home']} vs
        <img src='{team_logo(m["away"])}' width='25'>
        {m['away']} <br>
        AI šansa {m['chance']}% <br>
        Tip: {m['tip']}
        </div>
        """

    html+="</body></html>"

    return html


app.run(host="0.0.0.0",port=5000)
