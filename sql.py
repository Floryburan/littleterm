import os
from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

# MySQL 数据库连接配置
db_config = {
    "host": "localhost",
    "user": "your_db_user",
    "password": "your_db_password",
    "database": "your_db_name"
}

# 建立数据库连接
db_connection = mysql.connector.connect(**db_config)

# 创建数据库表格
def create_table():
    cursor = db_connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(255) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS classification_results (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            total_packets INT NOT NULL,
            malicious_packets INT NOT NULL,
            benign INT NOT NULL,
            dos INT NOT NULL,
            u2r INT NOT NULL,
            r21 INT NOT NULL,
            probe INT NOT NULL
        )
    """)
    db_connection.commit()
    cursor.close()

# 用户注册
@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data["username"]
    password = data["password"]

    # 检查用户名是否已存在
    cursor = db_connection.cursor()
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    existing_user = cursor.fetchone()

    if existing_user:
        return jsonify({"message": "Username already exists"})

    # 注册新用户
    cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
    db_connection.commit()
    cursor.close()

    return jsonify({"message": "Registration successful"})

# 用户登录
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data["username"]
    password = data["password"]

    cursor = db_connection.cursor()
    cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
    user = cursor.fetchone()
    cursor.close()

    if user:
        user_id, username, _ = user
        return jsonify({"user_id": user_id, "username": username})

    return jsonify({"message": "Invalid credentials"})

# 接收分类结果
@app.route("/classify", methods=["POST"])
def classify():
    data = request.get_json()
    user_id = data["user_id"]
    total_packets = data["total_packets"]
    malicious_packets = data["malicious_packets"]
    benign = data["benign"]
    dos = data["dos"]
    u2r = data["u2r"]
    r21 = data["r21"]
    probe = data["probe"]

    cursor = db_connection.cursor()
    cursor.execute("""
        INSERT INTO classification_results (user_id, total_packets, malicious_packets, benign, dos, u2r, r21, probe)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (user_id, total_packets, malicious_packets, benign, dos, u2r, r21, probe))
    db_connection.commit()
    cursor.close()

    # 计算每个分类在恶意流量总数的占比
    percentages = {
        "benign_percentage": (benign / malicious_packets) * 100,
        "dos_percentage": (dos / malicious_packets) * 100,
        "u2r_percentage": (u2r / malicious_packets) * 100,
        "r21_percentage": (r21 / malicious_packets) * 100,
        "probe_percentage": (probe / malicious_packets) * 100
    }

    return jsonify(percentages)

if __name__ == "__main__":
    create_table()
    app.run(debug=True)
