from flask import Flask
import random

app = Flask(__name__)

@app.route("/")
def home():
    return "AI SERVER RUNNING ⚽"

@app.route("/today")
def today():

    matches = [
        ("Barcelona", "Real Madrid"),
        ("Man City", "Arsenal"),
        ("PSG", "Marseille")
    ]

    results = []

    for home, away in matches:

        home_power = random.randint(60, 95)
        away_power = random.randint(60, 90)

        home_score = home_power + 5
        away_score = away_power

        total = home_score + away_score

        home_win = round((home_score / total) * 100, 1)
        away_win = round((away_score / total) * 100, 1)

        pick = home if home_win > away_win else away

        results.append({
            "match": f"{home} vs {away}",
            "home_%": home_win,
            "away_%": away_win,
            "pick": pick
        })

    return {"matches": results}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
