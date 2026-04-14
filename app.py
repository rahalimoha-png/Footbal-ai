from flask import Flask
import random

app = Flask(__name__)

@app.route("/")
def home():
    return "AI FOOTBALL RUNNING ⚽"

@app.route("/today")
def today():

    matches = [
        ("Barcelona", "Real Madrid"),
        ("Man City", "Arsenal"),
        ("PSG", "Marseille")
    ]

    results = []

    for home, away in matches:

        home_power = random.uniform(65, 95)
        away_power = random.uniform(60, 90)

        home_adv = 6

        home_score = home_power + home_adv
        away_score = away_power

        total = home_score + away_score

        home_win = round((home_score / total) * 100, 1)
        away_win = round((away_score / total) * 100, 1)

        pick = home if home_win > away_win else away

        results.append({
            "match": f"{home} vs {away}",
            "home_win_%": home_win,
            "away_win_%": away_win,
            "pick": pick
        })

    best = max(results, key=lambda x: abs(x["home_win_%"] - x["away_win_%"]))

    return {
        "matches": results,
        "best_pick": best
    }

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
