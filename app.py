from flask import Flask, render_template, request
import requests
import random

app = Flask(__name__)


# uzmi utakmice
def get_today_matches():

    url = "https://api.sofascore.com/api/v1/sport/football/events/live"

    matches = []

    try:
        r = requests.get(url)
        data = r.json()
    except:
        return matches

    for event in data.get("events", []):

        home = event["homeTeam"]["name"]
        away = event["awayTeam"]["name"]

        home_prob = random.randint(40, 75)
        draw_prob = random.randint(20, 40)
        away_prob = random.randint(40, 75)

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

    matches = sorted(matches, key=lambda x: x["prob"], reverse=True)

    return matches[:20]


# generisi tiket
def generate_ticket(matches):

    if len(matches) < 3:
        return []

    ticket = random.sample(matches, 3)

    return ticket


@app.route("/", methods=["GET", "POST"])
def home():

    matches = get_today_matches()

    tip = None
    ticket = None

    if matches:
        tip = matches[0]

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
