from flask import Flask, render_template
import os
import random
from datetime import datetime, timedelta

app = Flask(__name__)

# Lige koje nas zanimaju
LEAGUES = [
    "Premier League",
    "La Liga",
    "Serie A",
    "Bundesliga",
    "Ligue 1",
    "Super Lig",
    "Champions League"
]

# Primer utakmica za danas i sutra
MATCHES = {
    "Premier League": [
        ("Manchester City","Arsenal"),
        ("Liverpool","Chelsea")
    ],
    "La Liga": [
        ("Real Madrid","Sevilla"),
        ("Barcelona","Valencia")
    ],
    "Serie A": [
        ("Inter","Roma"),
        ("Juventus","Napoli")
    ],
    "Bundesliga": [
        ("Bayern","Dortmund"),
        ("Leipzig","Leverkusen")
    ],
    "Ligue 1": [
        ("PSG","Monaco"),
        ("Lyon","Marseille")
    ],
    "Super Lig": [
        ("Galatasaray","Besiktas"),
        ("Fenerbahce","Trabzonspor")
    ],
    "Champions League": [
        ("Real Madrid","Bayern"),
        ("Manchester City","Inter")
    ]
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


@app.route("/")
def home():

    leagues = {}

    for league, games in MATCHES.items():

        matches = []

        for m in games:

            tip, prob = ai_tip()

            matches.append({
                "home": m[0],
                "away": m[1],
                "tip": tip,
                "prob": prob
            })

        leagues[league] = matches

    today = datetime.now().strftime("%d.%m.%Y")
    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%d.%m.%Y")

    return render_template(
        "index.html",
        leagues=leagues,
        today=today,
        tomorrow=tomorrow
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT",10000))
    app.run(host="0.0.0.0", port=port)
