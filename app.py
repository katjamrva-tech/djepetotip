from flask import Flask, render_template, request
import requests
import random

app = Flask(__name__)


def fetch_matches():

    urls = [
        "https://api.sofascore.com/api/v1/sport/football/events/live",
        "https://api.sofascore.com/api/v1/sport/football/events/last/0"
    ]

    matches = []

    for url in urls:

        try:
            r = requests.get(url)
            data = r.json()
        except:
            continue

        for event in data.get("events", []):

            home = event["homeTeam"]["name"]
            away = event["awayTeam"]["name"]

            home_prob = random.randint(40,75)
            draw_prob = random.randint(20,40)
            away_prob = random.randint(40,75)

            if home_prob > draw_prob and home_prob > away_prob:
                tip = "1"
                prob = home_prob
            elif draw_prob > home_prob and draw_prob > away_prob:
                tip = "X"
                prob = draw_prob
            else:
                tip = "2"
                prob = away_prob

            matches.append({
                "home": home,
                "away": away,
                "tip": tip,
                "prob": prob
            })

    # ako API vrati malo utakmica
    if len(matches) < 20:

        teams = [
            "Arsenal","Chelsea","Liverpool","Tottenham",
            "Real Madrid","Barcelona","Atletico",
            "Inter","Milan","Juventus",
            "Bayern","Dortmund","Leipzig",
            "PSG","Lyon","Monaco"
        ]

        while len(matches) < 20:

            home = random.choice(teams)
            away = random.choice(teams)

            if home == away:
                continue

            prob = random.randint(55,75)

            if prob > 65:
                tip = "1"
            elif prob > 60:
                tip = "X"
            else:
                tip = "2"

            matches.append({
                "home": home,
                "away": away,
                "tip": tip,
                "prob": prob
            })

    matches = sorted(matches, key=lambda x: x["prob"], reverse=True)

    return matches[:20]


def generate_ticket(matches):

    if len(matches) < 3:
        return []

    return random.sample(matches, 3)


@app.route("/", methods=["GET","POST"])
def home():

    matches = fetch_matches()

    tip = matches[0]

    ticket = None

    if request.method == "POST":
        ticket = generate_ticket(matches)

    return render_template(
        "index.html",
        matches=matches,
        tip=tip,
        ticket=ticket
    )


if __name__ == "__main__":
    app.run(debug=True)
