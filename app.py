from flask import Flask, render_template, request
import requests
import random

app = Flask(__name__)

def get_matches():
    url = "https://site.api.espn.com/apis/site/v2/sports/soccer/eng.1/scoreboard"
    r = requests.get(url)
    data = r.json()

    matches = []

    if "events" in data:
        for event in data["events"]:
            home = event["competitions"][0]["competitors"][0]["team"]["name"]
            away = event["competitions"][0]["competitors"][1]["team"]["name"]

            prob = random.randint(55, 75)

            matches.append({
                "home": home,
                "away": away,
                "prob": prob
            })

    return matches


@app.route("/", methods=["GET","POST"])
def home():
    matches = get_matches()

    search_result = None

    if request.method == "POST":
        team = request.form.get("team")

        for m in matches:
            if team.lower() in m["home"].lower() or team.lower() in m["away"].lower():
                search_result = m

    tip = random.choice(matches) if matches else None

    return render_template(
        "index.html",
        matches=matches,
        tip=tip,
        search_result=search_result
    )


if __name__ == "__main__":
    app.run()

