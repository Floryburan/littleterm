import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import logging

app = Flask(__name__)

# 配置日志记录
log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(level=logging.INFO, format=log_format)
logger = logging.getLogger(__name__)

# 配置数据库连接
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
    label = db.Column(db.String(255), nullable=False)
    count = db.Column(db.Integer, nullable=False)

# 函数来创建数据库表格
def create_tables():
    with app.app_context():
        db.create_all()

# 用户注册
@app.route("/register", methods=["POST"])
def register():
    try:
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

    except KeyError as e:
        return jsonify({"error": f"Missing key in request data: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 用户登录
@app.route("/login", methods=["POST"])
def login():
    try:
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

    except KeyError as e:
        return jsonify({"error": f"Missing key in request data: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 接收分类结果
@app.route('/api/store_results', methods=['POST'])
def store_results():
    try:
        # 获取来自test.py的数据结果
        data = request.get_json()
        results = data.get('results', {})

        if not results:
            return jsonify({"error": "No results provided"}), 400

        # 计算恶意数据包总数
        malicious_packets = sum(results.values())

        # 使用数据库会话
        with db.session.begin() as transaction:
            for label, count in results.items():
                # 插入数据到数据库
                new_result = ClassificationResult(label=label, count=count)
                db.session.add(new_result)
            
            # 提交事务
            transaction.commit()

            # 计算每个标签在恶意数据包中的占比
            percentages = {label: (count / malicious_packets) * 100 for label, count in results.items()}

        # 返回分类数目和百分比信息给前端
        response_data = {
            "message": "Results stored successfully",
            "malicious_packets": malicious_packets,
            "percentages": percentages
        }

        return jsonify(response_data), 200

    except KeyError as e:
        return jsonify({"error": f"Missing key in request data: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # 创建数据库表格
    create_tables()
    app.run(debug=True)