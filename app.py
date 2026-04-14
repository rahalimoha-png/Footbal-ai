from flask import Flask
import requests
import os
import random

app = Flask(__name__)

@app.route("/")
def home():
    return "REAL AI FOOTBALL RUNNING ⚽"

@app.route("/today")
def today():

    API_KEY = os.environ.get("API_KEY")

    if not API_KEY:
        return {"error": "API KEY missing"}

    url = "https://api-football-v1.p.rapidapi.com/v3/fixtures?date=2024-04-14"

    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
    }

    try:
        res = requests.get(url, headers=headers).json()

        matches = []

        for m in res.get("response", [])[:5]:

            home = m["teams"]["home"]["name"]
            away = m["teams"]["away"]["name"]

            # 🧠 AI بسيط
            home_power = random.randint(60, 95)
            away_power = random.randint(60, 90)

            home_score = home_power + 5
            away_score = away_power

            total = home_score + away_score

            home_win = round((home_score / total) * 100, 1)
            away_win = round((away_score / total) * 100, 1)

            diff = abs(home_win - away_win)

            pick = home if home_win > away_win else away

            matches.append({
                "match": f"{home} vs {away}",
                "home_%": home_win,
                "away_%": away_win,
                "pick": pick,
                "confidence": diff
            })

        matches = sorted(matches, key=lambda x: x["confidence"], reverse=True)

        return {
            "best_pick": matches[0] if matches else {},
            "matches": matches
        }

    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
