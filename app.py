from flask import Flask, render_template, request
import requests
import random

app = Flask(__name__)


def get_today_matches():

    url = "https://api.sofascore.com/api/v1/sport/football/events/live"

    try:
        r = requests.get(url)
        data = r.json()
    except:
        return []

    matches = []

    for event in data.get("events", []):

        home = event["homeTeam"]["name"]
        away = event["awayTeam"]["name"]

        prob = random.randint(55,75)

        if prob >= 65:
            tip = "1"
        elif prob >= 60:
            tip = "X"
        else:
            tip = "2"

        matches.append({
            "home": home,
            "away": away,
            "tip": tip,
            "prob": prob
        })

    return matches


def best_matches():

    matches = get_today_matches()

    matches = sorted(matches, key=lambda x: x["prob"], reverse=True)

    return matches[:20]


def generate_ticket(matches):

    if len(matches) < 3:
        return None, None

    ticket = random.sample(matches, 3)

    total_prob = 1

    for m in ticket:
        total_prob *= m["prob"] / 100

    total_prob = round(total_prob * 100, 2)

    return ticket, total_prob


@app.route("/", methods=["GET","POST"])
def home():

    matches = best_matches()

    tip = matches[0] if matches else None

    ticket = None
    total_prob = None

    if request.method == "POST":
        ticket, total_prob = generate_ticket(matches)

    return render_template(
        "index.html",
        matches=matches,
        tip=tip,
        ticket=ticket,
        total_prob=total_prob
    )


if __name__ == "__main__":
    app.run(debug=True)
