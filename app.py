from flask import Flask, render_template
import requests
import os
import random
from datetime import datetime, timedelta

app = Flask(__name__)

LEAGUES = {
    "Premier League": "eng.1",
    "La Liga": "esp.1",
    "Serie A": "ita.1",
    "Bundesliga": "ger.1",
    "Ligue 1": "fra.1",
    "Super Lig": "tur.1",
    "UEFA Champions League": "uefa.champions"
}


def ai_tip():

    home = random.randint(40,75)
    draw = random.randint(20,40)
    away = random.randint(40,75)

    if home > draw and home > away:
        return "1", home
    elif draw > home and draw > away:
        return "X", draw
    else:
        return "2", away


def get_matches(code):

    url = f"https://site.api.espn.com/apis/site/v2/sports/soccer/{code}/scoreboard"

    matches = []

    try:

        r = requests.get(url, timeout=10)
        data = r.json()

        for event in data.get("events", []):

            comp = event["competitions"][0]
            teams = comp["competitors"]

            home = teams[0]["team"]["displayName"]
            away = teams[1]["team"]["displayName"]

            date = event["date"][:10]

            tip, prob = ai_tip()

            matches.append({
                "home": home,
                "away": away,
                "tip": tip,
                "prob": prob,
                "date": date
            })

    except:
        pass

    return matches


@app.route("/")
def home():

    leagues = {}

    today = datetime.utcnow().date()
    tomorrow = today + timedelta(days=1)

    for league, code in LEAGUES.items():

        games = []

        matches = get_matches(code)

        for m in matches:

            try:
                match_date = datetime.fromisoformat(m["date"]).date()
            except:
                continue

            if match_date == today or match_date == tomorrow:
                games.append(m)

        leagues[league] = games

    return render_template("index.html", leagues=leagues)


if __name__ == "__main__":

    port = int(os.environ.get("PORT",10000))
    app.run(host="0.0.0.0", port=port)
