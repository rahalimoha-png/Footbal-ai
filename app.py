from flask import Flask
import requests
import os
import random
from datetime import datetime

app = Flask(__name__)

API_KEY = os.environ.get("API_KEY")


# 🏠 واجهة رئيسية
@app.route("/")
def home():
    return """
    <html>
    <head>
        <title>AI Football Pro</title>
        <style>
            body{font-family:Arial;background:#0f172a;color:white;text-align:center}
            .box{background:#1e293b;margin:20px;padding:20px;border-radius:12px}
            a{color:#38bdf8;font-size:22px;text-decoration:none}
        </style>
    </head>
    <body>
        <h1>⚽ AI FOOTBALL PRO SYSTEM</h1>
        <div class="box">
            <p>Daily Smart Predictions + Tickets</p>
            <a href="/ticket">🔥 GET TODAY TICKET</a>
        </div>
    </body>
    </html>
    """


# 📊 API JSON
@app.route("/api")
def api():

    if not API_KEY:
        return {"error": "API KEY missing"}

    date = datetime.today().strftime('%Y-%m-%d')

    url = f"https://api-football-v1.p.rapidapi.com/v3/fixtures?date={date}"

    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
    }

    res = requests.get(url, headers=headers).json()

    matches = []

    for m in res.get("response", [])[:7]:

        home = m["teams"]["home"]["name"]
        away = m["teams"]["away"]["name"]

        home_power = random.randint(60, 95)
        away_power = random.randint(60, 90)

        home_score = home_power + 5
        away_score = away_power

        total = home_score + away_score

        home_pct = round((home_score / total) * 100, 1)
        away_pct = round((away_score / total) * 100, 1)

        pick = home if home_pct > away_pct else away

        matches.append({
            "match": f"{home} vs {away}",
            "home_win_%": home_pct,
            "away_win_%": away_pct,
            "pick": pick
        })

    best = max(matches, key=lambda x: abs(x["home_win_%"] - x["away_win_%"])) if matches else {}

    return {
        "date": date,
        "matches": matches,
        "best_pick": best
    }


# 🎯 تيكي يومي (واجهة جميلة)
@app.route("/ticket")
def ticket():

    if not API_KEY:
        return "API KEY missing"

    date = datetime.today().strftime('%Y-%m-%d')

    url = f"https://api-football-v1.p.rapidapi.com/v3/fixtures?date={date}"

    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
    }

    res = requests.get(url, headers=headers).json()

    matches = res.get("response", [])[:7]

    html = """
    <html>
    <head>
        <title>Daily Ticket</title>
        <style>
            body{font-family:Arial;background:#111827;color:white;text-align:center}
            .card{background:#1f2937;margin:15px;padding:15px;border-radius:10px}
            .pick{color:#22c55e;font-size:20px}
        </style>
    </head>
    <body>
        <h1>🎯 TODAY AI TICKET</h1>
    """

    picks = []

    for m in matches:

        home = m["teams"]["home"]["name"]
        away = m["teams"]["away"]["name"]

        home_score = random.randint(60, 95)
        away_score = random.randint(60, 90)

        pick = home if home_score > away_score else away

        picks.append(pick)

        html += f"""
        <div class="card">
            <h3>{home} vs {away}</h3>
            <p>Prediction: <b class="pick">{pick}</b></p>
        </div>
        """

    best_ticket = picks[0] if picks else "No matches"

    html += f"""
        <h2>🔥 BEST TICKET: {best_ticket}</h2>
        <br><a href="/">⬅ Back</a>
    </body>
    </html>
    """

    return html


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
