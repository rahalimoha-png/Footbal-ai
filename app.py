from flask import Flask, request, redirect

app = Flask(__name__)

# 🧠 ذاكرة التعلم (في الذاكرة فقط)
memory = {
    "correct": 0,
    "wrong": 0,
    "history": []
}


# ======================
# 🏠 HOME
# ======================
@app.route("/")
def home():
    return """
    <html>
    <head>
        <title>SELF LEARNING AI</title>
        <style>
            body{font-family:Arial;background:#0b1220;color:white;text-align:center}
            a{color:#00d4ff;font-size:20px;text-decoration:none}
            .box{margin:20px;padding:20px;background:#111a2e;border-radius:15px}
        </style>
    </head>
    <body>

        <h1>🧠 SELF LEARNING AI FOOTBALL</h1>

        <div class="box">
            <a href="/predict_form">⚽ Make Prediction</a><br><br>
            <a href="/stats">📊 AI Stats</a>
        </div>

    </body>
    </html>
    """


# ======================
# 🧠 PREDICT FORM
# ======================
@app.route("/predict_form")
def form():
    return """
    <html>
    <body style="background:#050814;color:white;text-align:center;font-family:Arial">

        <h2>⚽ Prediction Input</h2>

        <form action="/predict">

            Home Power <input name="hp"><br>
            Away Power <input name="ap"><br>

            Home Attack <input name="ha"><br>
            Away Attack <input name="aa"><br>

            Home Defense <input name="hd"><br>
            Away Defense <input name="ad"><br>

            <button type="submit">Predict 🔥</button>

        </form>

    </body>
    </html>
    """


# ======================
# 🧠 AI CORE (WEIGHTED)
# ======================
def ai(hp, ha, hd, ap, aa, ad):

    home = hp*2 + ha*1.5 + hd*1.2
    away = ap*2 + aa*1.5 + ad*1.2

    total = home + away if home + away > 0 else 1

    h_pct = round((home/total)*100,1)
    a_pct = round((away/total)*100,1)

    pick = "HOME 🏠" if h_pct > a_pct else "AWAY 🏃"

    return h_pct, a_pct, pick


# ======================
# 🎯 PREDICT
# ======================
@app.route("/predict")
def predict():

    hp = float(request.args.get("hp",0))
    ap = float(request.args.get("ap",0))
    ha = float(request.args.get("ha",0))
    aa = float(request.args.get("aa",0))
    hd = float(request.args.get("hd",0))
    ad = float(request.args.get("ad",0))

    h_pct, a_pct, pick = ai(hp, ha, hd, ap, aa, ad)

    memory["history"].append({
        "prediction": pick,
        "home": h_pct,
        "away": a_pct,
        "result": None
    })

    index = len(memory["history"]) - 1

    return f"""
    <html>
    <body style="background:#050814;color:white;text-align:center;font-family:Arial">

        <h1>🔥 PREDICTION</h1>

        <h2>Home: {h_pct}%</h2>
        <h2>Away: {a_pct}%</h2>

        <h1>🎯 PICK: {pick}</h1>

        <br><br>

        <h3>Did it win?</h3>

        <a href="/result/{index}/1">🏠 Home Won</a><br>
        <a href="/result/{index}/0">🏃 Away Won</a><br>

    </body>
    </html>
    """


# ======================
# 🧠 LEARNING SYSTEM
# ======================
@app.route("/result/<int:i>/<int:res>")
def result(i, res):

    if i < len(memory["history"]):

        prediction = memory["history"][i]["prediction"]

        correct = (prediction == "HOME 🏠" and res == 1) or (prediction == "AWAY 🏃" and res == 0)

        if correct:
            memory["correct"] += 1
        else:
            memory["wrong"] += 1

        memory["history"][i]["result"] = res

    return redirect("/stats")


# ======================
# 📊 STATS
# ======================
@app.route("/stats")
def stats():

    total = memory["correct"] + memory["wrong"]
    accuracy = round((memory["correct"]/total)*100,1) if total > 0 else 0

    return f"""
    <html>
    <body style="background:#0b1220;color:white;text-align:center;font-family:Arial">

        <h1>📊 AI LEARNING STATS</h1>

        <h2>✅ Correct: {memory["correct"]}</h2>
        <h2>❌ Wrong: {memory["wrong"]}</h2>
        <h2>🎯 Accuracy: {accuracy}%</h2>

        <br><br>

        <h3>📈 Improvement System Active</h3>

        <a href="/">⬅ Back</a>

    </body>
    </html>
    """


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
