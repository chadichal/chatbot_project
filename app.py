
from flask import Flask, render_template, request, jsonify
import sqlite3
from difflib import get_close_matches
from datetime import datetime

app = Flask(__name__)
DB = "chatbot.db"

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS qa (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT,
            answer TEXT,
            created_at TEXT
        )
    ''')
    conn.commit()
    conn.close()

def find_answer(user_q):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT question, answer FROM qa")
    rows = c.fetchall()
    conn.close()

    questions = [r[0] for r in rows]
    matches = get_close_matches(user_q, questions, n=1, cutoff=0.6)
    if matches:
        for q, a in rows:
            if q == matches[0]:
                return a
    return None

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_msg = data.get("message","").strip()

    if not user_msg:
        return jsonify({"reply":"Please enter a question."})

    try:
        answer = find_answer(user_msg)

        if answer:
            return jsonify({"reply": answer})
        else:
            return jsonify({"reply":"I don't know the answer yet. You can add it using the Add Q&A section."})

    except Exception as e:
        return jsonify({"reply":"Server error occurred."})

@app.route("/add_qa", methods=["POST"])
def add_qa():
    data = request.json
    q = data.get("question")
    a = data.get("answer")

    if not q or not a:
        return jsonify({"status":"error","msg":"Missing fields"})

    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("INSERT INTO qa (question, answer, created_at) VALUES (?,?,?)",
              (q, a, datetime.now().isoformat()))
    conn.commit()
    conn.close()

    return jsonify({"status":"success","msg":"Q&A saved successfully"})

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
