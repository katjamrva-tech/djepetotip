from flask import Flask, render_template
import requests
import os
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


def ai_tip(home, away):

    seed = abs(hash(home + away)) % 100

    home_prob = 40 + (seed % 30)
    draw_prob = 20 + (seed % 20)
    away_prob = 40 + ((seed * 2) % 30)

    if home_prob > draw_prob and home_prob > away_prob:
        return "1", home_prob
    elif draw_prob > home_prob and draw_prob > away_prob:
        return "X", draw_prob
    else:
        return "2", away_prob


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

            home_logo = teams[0]["team"]["logo"]
            away_logo = teams[1]["team"]["logo"]

            date = event["date"][:10]

            tip, prob = ai_tip(home, away)

            matches.append({
                "home": home,
                "away": away,
                "home_logo": home_logo,
                "away_logo": away_logo,
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
