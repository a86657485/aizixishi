from flask import Flask, request, jsonify
import sqlite3, json, os
from datetime import datetime

app = Flask(__name__)
DB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "survey.db")

def init_db():
    with sqlite3.connect(DB) as conn:
        conn.execute("CREATE TABLE IF NOT EXISTS surveys (id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp TEXT, data TEXT)")

@app.after_request
def cors(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return response

@app.route("/api/submit", methods=["POST", "OPTIONS"])
def submit():
    if request.method == "OPTIONS": return "", 200
    body = request.get_json(force=True)
    ts = body.get("timestamp", datetime.now().isoformat())
    with sqlite3.connect(DB) as conn:
        conn.execute("INSERT INTO surveys (timestamp, data) VALUES (?, ?)", (ts, json.dumps(body, ensure_ascii=False)))
    return jsonify({"success": True, "message": "ok"})

@app.route("/api/data", methods=["GET"])
def data():
    with sqlite3.connect(DB) as conn:
        rows = conn.execute("SELECT id, timestamp, data FROM surveys ORDER BY id DESC").fetchall()
    result = []
    for r in rows:
        item = {"id": r[0], "timestamp": r[1]}
        try: item.update(json.loads(r[2]))
        except: pass
        result.append(item)
    return jsonify(result)

@app.route("/api/data/<int:id>", methods=["DELETE", "OPTIONS"])
def delete(id):
    if request.method == "OPTIONS": return "", 200
    with sqlite3.connect(DB) as conn:
        conn.execute("DELETE FROM surveys WHERE id = ?", (id,))
    return jsonify({"success": True})

@app.route("/api/stats", methods=["GET"])
def stats():
    with sqlite3.connect(DB) as conn:
        rows = conn.execute("SELECT data FROM surveys").fetchall()
    stats_data = {"total": len(rows), "recent_7_days": len(rows),
        "by_subject": {}, "by_experience": {}, "by_grade": {},
        "big_screen": {}, "ai_features": {}, "ipad_features": {}, "ipad_worry": {},
        "willingness": {}}
    for (d,) in rows:
        try: d = json.loads(d)
        except: continue
        for k in ["q1","q2","q3"]:
            key = {"q1":"by_subject","q2":"by_experience","q3":"by_grade"}[k]
            for v in (d.get(k) or []): stats_data[key][v] = stats_data[key].get(v, 0) + 1
        for k in ["q7a","q7b","q7c","q7d","q9a","q9b","q9c","q9d","q11a","q11b","q11c","q11d","q11e"]:
            for v in (d.get(k) or []):
                stats_data["big_screen" if k.startswith("q7") else ("ai_features" if k.startswith("q9") else "ipad_features")][v] = \
                    stats_data.get("big_screen" if k.startswith("q7") else ("ai_features" if k.startswith("q9") else "ipad_features"), {}).get(v, 0) + 1
        for v in (d.get("q12") or []): stats_data["ipad_worry"][v] = stats_data["ipad_worry"].get(v, 0) + 1
        if d.get("q15"): stats_data["willingness"][str(d["q15"])] = stats_data["willingness"].get(str(d["q15"]), 0) + 1
    return jsonify(stats_data)

init_db()
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
