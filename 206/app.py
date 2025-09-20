from flask import Flask, render_template, jsonify
import json
import os

app = Flask(__name__)

@app.route("/")
def index():
    timeline = []
    if os.path.exists("timeline.json"):
        with open("timeline.json", "r", encoding="utf-8") as f:
            try:
                timeline = json.load(f)
            except json.JSONDecodeError:
                timeline = []

    # timestamp 순으로 정렬
    timeline = sorted(timeline, key=lambda x: x["timestamp"])

    return render_template("index.html", timeline=timeline)


if __name__ == "__main__":
    app.run(debug=True)
