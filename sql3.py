import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy  # 使用 SQLAlchemy 来简化数据库操作
from werkzeug.security import generate_password_hash, check_password_hash  # 密码哈希化
import logging  # 导入日志模块

app = Flask(__name__)

# 配置日志记录
log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(level=logging.INFO, format=log_format)
logger = logging.getLogger(__name__)

# 使用配置文件来管理敏感信息
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123456@192.168.211.1:3306/sql2'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123456@localhost/sql2'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# 定义数据库模型
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

class ClassificationResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    total_packets = db.Column(db.Integer, nullable=False)
    malicious_packets = db.Column(db.Integer, nullable=False)
    normal_packets = db.Column(db.Integer, nullable=False) 
    benign = db.Column(db.Integer, nullable=False)
    dos = db.Column(db.Integer, nullable=False)
    u2r = db.Column(db.Integer, nullable=False)
    r21 = db.Column(db.Integer, nullable=False)
    probe = db.Column(db.Integer, nullable=False)

# 函数来创建数据库表格
def create_tables():
    with app.app_context():
        db.create_all()


# 用户注册
@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data["username"]
    password = data["password"]

    # 检查用户名是否已存在
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        logger.info(f"Registration failed: Username {username} already exists")
        return jsonify({"message": "Username already exists"})

    # 哈希化密码
    password_hash = generate_password_hash(password)

    # 注册新用户
    new_user = User(username=username, password_hash=password_hash)
    db.session.add(new_user)
    db.session.commit()
    logger.info(f"Registration successful: User {username} registered")
    return jsonify({"message": "Registration successful"})

# 用户登录
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data["username"]
    password = data["password"]

    # 查找用户
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password_hash, password):
        logger.info(f"Login successful: User {username} logged in")
        return jsonify({"user_id": user.id, "username": user.username})

    logger.info(f"Login failed: Invalid credentials for user {username}")
    return jsonify({"message": "Invalid credentials"})

# 接收分类结果
# http://192.168.211.1:5000//calculate
@app.route("/calculate", methods=["POST"])
def calculate():
    data = request.get_json()
    malicious_packets = data["malicious_packets"]
    normal_packets = data["normal_packets"]
    benign = data["benign"]
    dos = data["dos"]
    u2r = data["u2r"]
    r21 = data["r21"]
    probe = data["probe"]
    
    total_packets = malicious_packets + normal_packets

   # 计算正常流量的占比和每个分类在恶意流量总数的占比
    percentages = {
        "normal_percentage": (normal_packets / total_packets) * 100,
        "benign_percentage": (benign / malicious_packets) * 100,
        "dos_percentage": (dos / malicious_packets) * 100,
        "u2r_percentage": (u2r / malicious_packets) * 100,
        "r21_percentage": (r21 / malicious_packets) * 100,
        "probe_percentage": (probe / malicious_packets) * 100
    }

    return jsonify({
        "total_packets": total_packets,
        "malicious_packets": malicious_packets,
        "normal_packets": normal_packets,
        "benign": benign,
        "dos": dos,
        "u2r": u2r,
        "r21": r21,
        "probe": probe,
        "percentages": percentages
    })

if __name__ == "__main__":
    # 创建数据库表格
    create_tables()
    app.run(debug=True)