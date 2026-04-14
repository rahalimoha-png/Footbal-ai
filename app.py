from flask import Flask, request, jsonify

app = Flask(__name__)

def ai_model(home_team, away_team):

    # ⚽ بيانات “ذكية” مبسطة (نقدر نطوروها لاحقًا ببيانات حقيقية)
    import random

    home_strength = random.uniform(60, 90)
    away_strength = random.uniform(50, 85)

    home_adv = 8
    away_adv = 0

    home_score = home_strength + home_adv
    away_score = away_strength + away_adv

    total = home_score + away_score

    home_win = round((home_score / total) * 100, 1)
    away_win = round((away_score / total) * 100, 1)

    if home_win > 55:
        pick = home_team
        verdict = "🔥 مرشح قوي للفوز"
    elif away_win > 55:
        pick = away_team
        verdict = "⚽ مفاجأة خارج الديار"
    else:
        pick = "تعادل"
        verdict = "🤝 مباراة خطيرة"

    risk = "🎯 آمن" if abs(home_win - away_win) > 20 else "💣 خطر"

    return {
        "match": f"{home_team} vs {away_team}",
        "home_win_%": home_win,
        "away_win_%": away_win,
        "prediction": pick,
        "analysis": verdict,
        "risk": risk
    }

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json
    return jsonify(ai_model(data["home_team"], data["away_team"]))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
