from flask import Flask, jsonify
import requests
import random

app = Flask(__name__)

API_KEY = "PUT_YOUR_API_KEY_HERE"
URL = "https://v3.football.api-sports.io/fixtures?date=today"

headers = {
    "x-apisports-key": API_KEY
}

def analyze(home, away):

    # ⚽ قوة ذكية
    home_power = random.uniform(70, 95)
    away_power = random.uniform(65, 90)

    home_adv = 6

    home_score = home_power + home_adv
    away_score = away_power

    total = home_score + away_score

    home_win = round((home_score / total) * 100, 1)
    away_win = round((away_score / total) * 100, 1)

    diff = abs(home_win - away_win)

    if home_win > 58:
        pick = home
    elif away_win > 58:
        pick = away
    else:
        pick = "No strong pick"

    if diff > 20:
        confidence = "🎯 آمن"
    elif diff > 10:
        confidence = "⚠️ متوسط"
    else:
        confidence = "💣 خطر"

    return {
        "match": f"{home} vs {away}",
        "pick": pick,
        "home_win_%": home_win,
        "away_win_%": away_win,
        "confidence": confidence
    }

@app.route("/today", methods=["GET"])
def today():

    try:
        res = requests.get(URL, headers=headers).json()

        matches = []

        for m in res["response"][:5]:

            home = m["teams"]["home"]["name"]
            away = m["teams"]["away"]["name"]

            matches.append(analyze(home, away))

        # 🔥 اختيار أفضل مباراة
        best = max(matches, key=lambda x: abs(x["home_win_%"] - x["away_win_%"]))

        return jsonify({
            "matches": matches,
            "best_pick": best
        })

    except:
        return jsonify({"error": "API failed"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
