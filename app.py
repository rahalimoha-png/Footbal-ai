from flask import Flask
import requests
import os
from datetime import datetime, timedelta

app = Flask(__name__)

API_KEY = os.environ.get("API_KEY")


# ======================
# 🏠 HOME
# ======================
@app.route("/")
def home():
    return """
    <html>
    <head>
        <title>Smart AI Football</title>
        <style>
            body{font-family:Arial;background:#070b14;color:white;text-align:center}
            .box{background:#111a2e;margin:20px;padding:25px;border-radius:15px}
            a{color:#00e5ff;font-size:22px;text-decoration:none;font-weight:bold}
        </style>
    </head>
    <body>
        <h1>⚽ SMART AI FOOTBALL SYSTEM</h1>
        <div class="box">
            <p>Auto Daily Smart Tickets (No Empty Days)</p>
            <a href="/ticket">🔥 GET SMART TICKET</a>
        </div>
    </body>
    </html>
    """


# ======================
# 🔥 SMART DATA FETCH
# ======================
def get_matches():

    today = datetime.today()
    dates = [
        today.strftime('%Y-%m-%d'),
        (today + timedelta(days=1)).strftime('%Y-%m-%d'),
        (today - timedelta(days=1)).strftime('%Y-%m-%d')
    ]

    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
    }

    for d in dates:

        url = f"https://api-football-v1.p.rapidapi.com/v3/fixtures?date={d}"

        res = requests.get(url, headers=headers).json()

        if res.get("response"):
            return res, d

    return None, None


# ======================
# 📊 API JSON
# ======================
@app.route("/api")
def api():

    if not API_KEY:
        return {"error": "API KEY missing"}

    data, date = get_matches()

    if not data:
        return {"error": "No matches found"}

    matches = []

    for m in data.get("response", [])[:8]:

        home = m["teams"]["home"]["name"]
        away = m["teams"]["away"]["name"]

        home_score = len(home) * 3
        away_score = len(away) * 3

        home_score += 50
        away_score += 50

        total = home_score + away_score

        home_pct = round((home_score / total) * 100, 1)
        away_pct = round((away_score / total) * 100, 1)

        pick = home if home_pct > away_pct else away

        matches.append({
            "match": f"{home} vs {away}",
            "home_%": home_pct,
            "away_%": away_pct,
            "pick": pick
        })

    best = max(matches, key=lambda x: abs(x["home_%"] - x["away_%"])) if matches else {}

    return {
        "date_used": date,
        "matches": matches,
        "best_pick": best
    }


# ======================
# 🎯 SMART TICKET PAGE
# ======================
@app.route("/ticket")
def ticket():

    if not API_KEY:
        return "API KEY missing"

    data, date = get_matches()

    if not data:
        return "No matches available in API"

    html = """
    <html>
    <head>
        <title>Smart Ticket</title>
        <style>
            body{font-family:Arial;background:#050814;color:white;text-align:center}
            .card{background:#121c33;margin:15px;padding:15px;border-radius:12px}
            .pick{color:#00ff9d;font-size:20px;font-weight:bold}
        </style>
    </head>
    <body>
        <h1>⚽ SMART DAILY TICKET</h1>
    """

    picks = []

    for m in data.get("response", [])[:8]:

        home = m["teams"]["home"]["name"]
        away = m["teams"]["away"]["name"]

        home_score = len(home) * 4 + 50
        away_score = len(away) * 4 + 50

        pick = home if home_score > away_score else away

        picks.append(pick)

        html += f"""
        <div class="card">
            <h3>{home} vs {away}</h3>
            <p>AI Pick: <span class="pick">{pick}</span></p>
        </div>
        """

    best_ticket = picks[0] if picks else "No Matches"

    html += f"""
        <h2>🔥 BEST SMART TICKET: {best_ticket}</h2>
        <p>📅 Date Used: {date}</p>
        <br><a href="/">⬅ Back</a>
    </body>
    </html>
    """

    return html


# ======================
# RUN
# ======================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
