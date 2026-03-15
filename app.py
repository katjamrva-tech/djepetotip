from flask import Flask, render_template, request
import random
import os

app = Flask(__name__)

teams = [
"Arsenal","Chelsea","Liverpool","Tottenham",
"Manchester United","Manchester City",
"Real Madrid","Barcelona","Atletico Madrid",
"Inter","Milan","Juventus",
"Bayern Munich","Borussia Dortmund","RB Leipzig",
"PSG","Lyon","Monaco"
]

def generate_matches():

    matches = []

    for i in range(20):

        home = random.choice(teams)
        away = random.choice(teams)

        while home == away:
            away = random.choice(teams)

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

    matches = sorted(matches, key=lambda x: x["prob"], reverse=True)

    return matches


def generate_ticket(matches):

    return random.sample(matches,3)


@app.route("/", methods=["GET","POST"])
def home():

    matches = generate_matches()

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
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
