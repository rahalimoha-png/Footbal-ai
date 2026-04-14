from flask import Flask, jsonify
import requests
import os

app = Flask(__name__)

API_KEY = os.getenv("08c67418b0411043bc7dab3af28068c8", "")

URL = "https://v3.football.api-sports.io/fixtures?date=today"

headers = {
    "x-apisports-key": API_KEY
}

@app.route("/today", methods=["GET"])
def today():

    if API_KEY == "":
        return jsonify({"error": "API KEY missing"})

    try:
        res = requests.get(URL, headers=headers).json()

        matches = []

        for m in res["response"][:5]:

            home = m["teams"]["home"]["name"]
            away = m["teams"]["away"]["name"]

            matches.append({
                "match": f"{home} vs {away}"
            })

        return jsonify(matches)

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
