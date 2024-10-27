from flask import Flask, jsonify, request
import sqlite3
import os
import datetime
import random
import string
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/hello-world", methods=["GET"])
def hello_world():
    return jsonify({"message": "Hello World"})



# secret key for jwt
SECRET_KEY = "secretkey"

# database path
DATABASE = "./database.db"


@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    if not username or not password:
        return jsonify({"error": "Missing username or password"}), 400

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = cursor.fetchone()
    if not user:
        return jsonify({"error": "Invalid username or password"}), 401


    
    token = ''.join(random.choices(string.ascii_letters + string.digits, k=16))

    cursor.execute("UPDATE users SET token=? WHERE id=?", (token, user[0]))
    conn.commit()

    payload = {
        "user_id": user[0],
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    }

    cursor.execute("SELECT * FROM users WHERE id=?", (user[0],))
    user = cursor.fetchone()
    return jsonify({"token": token, "user": user}), 200
if __name__ == "__main__":
    app.run(debug=True)
