from flask import Flask
import requests
import os
import random

app = Flask(__name__)

API_KEY = os.environ.get("08c67418b0411043bc7dab3af28068c8")

URL = "https://v3.football.api-sports.io/fixtures?date=today"

headers = {
    "x-apisports-key": API_KEY
}

@app.route("/")
def home():
    return "REAL AI FOOTBALL RUNNING ⚽"

@app.route("/today")
def today():

    if not API_KEY:
        return {"error": "API KEY missing"}

    try:
        res = requests.get(URL, headers=headers).json()

        matches = []

        for m in res.get("response", [])[:5]:

            home = m["teams"]["home"]["name"]
            away = m["teams"]["away"]["name"]

            # AI تحليل بسيط
            home_power = random.uniform(65, 95)
            away_power = random.uniform(60, 90)

            home_adv = 6

            home_score = home_power + home_adv
            away_score = away_power

            total = home_score + away_score

            home_win = round((home_score / total) * 100, 1)
            away_win = round((away_score / total) * 100, 1)

            pick = home if home_win > away_win else away

            matches.append({
                "match": f"{home} vs {away}",
                "home_win_%": home_win,
                "away_win_%": away_win,
                "pick": pick
            })

        best = max(matches, key=lambda x: abs(x["home_win_%"] - x["away_win_%"]))

        return {
            "matches": matches,
            "best_pick": best
        }

    except Exception as e:
        return {"error": str(e)}
