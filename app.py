from flask import Flask
import requests
import os
from datetime import datetime

app = Flask(__name__)

API_KEY = os.environ.get("API_KEY")


# =========================
# 🏠 DASHBOARD
# =========================
@app.route("/")
def home():
    return """
    <html>
    <head>
        <title>AI FOOTBALL GLOBAL</title>
        <style>
            body{font-family:Arial;background:#070b14;color:white;text-align:center}
            .box{background:#111a2e;margin:20px;padding:25px;border-radius:15px}
            a{color:#00e5ff;font-size:22px;text-decoration:none;font-weight:bold}
        </style>
    </head>
    <body>
        <h1>🌍 AI FOOTBALL GLOBAL SYSTEM</h1>
        <div class="box">
            <p>Smart AI Predictions + Real Stats + Daily Tickets</p>
            <a href="/ticket">🔥 START GLOBAL TICKET</a>
        </div>
    </body>
    </html>
    """


# =========================
# 📊 GLOBAL API
# =========================
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

    for m in res.get("response", [])[:8]:

        fixture_id = m["fixture"]["id"]

        home = m["teams"]["home"]["name"]
        away = m["teams"]["away"]["name"]

        stats_url = f"https://api-football-v1.p.rapidapi.com/v3/fixtures/statistics?fixture={fixture_id}"
        stats_res = requests.get(stats_url, headers=headers).json()

        home_score = 50
        away_score = 50

        # 📊 تحليل الإحصائيات الحقيقية
        if stats_res.get("response"):
            for team in stats_res["response"]:
                for stat in team["statistics"]:

                    value = stat["value"]
                    if value is None:
                        continue

                    try:
                        v = float(str(value).replace("%",""))
                    except:
                        v = 0

                    if team["team"]["name"] == home:
                        home_score += v
                    else:
                        away_score += v

        total = home_score + away_score if (home_score + away_score) > 0 else 1

        home_pct = round((home_score / total) * 100, 1)
        away_pct = round((away_score / total) * 100, 1)

        confidence = abs(home_pct - away_pct)

        pick = home if home_pct > away_pct else away

        matches.append({
            "match": f"{home} vs {away}",
            "home_%": home_pct,
            "away_%": away_pct,
            "confidence": confidence,
            "pick": pick
        })

    matches = sorted(matches, key=lambda x: x["confidence"], reverse=True)

    return {
        "date": date,
        "best_pick": matches[0] if matches else {},
        "matches": matches
    }


# =========================
# 🎯 GLOBAL TICKET PAGE
# =========================
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

    matches = res.get("response", [])[:8]

    html = """
    <html>
    <head>
        <title>Global Ticket</title>
        <style>
            body{font-family:Arial;background:#050814;color:white;text-align:center}
            .card{background:#121c33;margin:15px;padding:15px;border-radius:12px}
            .pick{color:#00ff9d;font-size:20px;font-weight:bold}
        </style>
    </head>
    <body>
        <h1>🌍 GLOBAL AI TICKET</h1>
    """

    picks = []

    for m in matches:

        home = m["teams"]["home"]["name"]
        away = m["teams"]["away"]["name"]

        home_score = 50
        away_score = 50

        try:
            home_score += len(home)
            away_score += len(away)
        except:
            pass

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
        <h2>🔥 GLOBAL BEST TICKET: {best_ticket}</h2>
        <br><a href="/">⬅ Back</a>
    </body>
    </html>
    """

    return html


# =========================
# RUN
# =========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
