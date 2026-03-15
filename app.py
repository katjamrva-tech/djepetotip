from flask import Flask, render_template
import requests
import random
import os
from datetime import datetime, timedelta

app = Flask(__name__)

LEAGUES = [
"Premier League",
"La Liga",
"Serie A",
"Bundesliga",
"Ligue 1",
"Super Lig",
"UEFA Champions League"
]


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


def get_matches():

    matches = []

    try:

        url = "https://api.sofascore.com/api/v1/sport/football/events/live"

        r = requests.get(url)

        data = r.json()

        for event in data.get("events", []):

            home = event["homeTeam"]["name"]
            away = event["awayTeam"]["name"]
            league = event["tournament"]["name"]

            if not any(l in league for l in LEAGUES):
                continue

            tip, prob = ai_tip()

            matches.append({
                "home": home,
                "away": away,
                "league": league,
                "tip": tip,
                "prob": prob
            })

    except:
        pass

    return matches


@app.route("/")
def home():

    matches = get_matches()

    leagues = {}

    for league in LEAGUES:
        leagues[league] = [m for m in matches if league in m["league"]]

    return render_template("index.html", leagues=leagues)


if __name__ == "__main__":
    port = int(os.environ.get("PORT",10000))
    app.run(host="0.0.0.0", port=port)
