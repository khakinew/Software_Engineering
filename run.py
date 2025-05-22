from flask import Flask, render_template, redirect, url_for, request, jsonify, abort
from flask_cors import CORS
from flask_login import (
    login_user,
    logout_user,
    login_required,
    current_user,
)
from utils.utils import jwt_required,generate_jwt
from extensions.error_handlers import register_error_handlers
from models.models import *
from config import Config
from api import api
import requests
app = Flask(__name__)
app.config.from_object(Config)
CORS(app, supports_credentials=True) 
db.init_app(app)
login_manager.init_app(app)
register_error_handlers(app)
app.register_blueprint(api)
@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    return render_template('index.html')

@app.route('/underwater', methods=['GET', 'POST'])
@login_required
def underwater():
    return render_template('underwater.html')

@app.route('/smart_center', methods=['GET', 'POST'])
@login_required
def smart_center():
    return render_template('smart_center.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            data = request.get_json(force=True)
        except Exception as e:
            return jsonify({"success": False, "message": "Invalid JSON data"}), 400

        if not data:
            return jsonify({"success": False, "message": "Missing JSON data"}), 400

        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({"success": False, "message": "用户名或密码不能为空"}), 400

        user = User.query.filter_by(username=username).first()
        if user and user.verify_password(password):
            login_user(user)
            token=generate_jwt(user.to_dict())
            return jsonify({
                "success": True,
                "user": user.to_dict(),
                "token": token,
                "message": "登录成功"
            })
        else:
            return jsonify({"success": False, "message": "用户名或密码错误"}), 401

    # 处理GET请求（如果有）
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            data = request.get_json(force=True)
        except Exception as e:
            return jsonify({"success": False, "message": "Invalid JSON data"}), 400

        if not data:
            return jsonify({"success": False, "message": "Missing JSON data"}), 400

        username = data.get('username')
        password = data.get('password')
        repassword = data.get('repassword')

        if not all([username, password, repassword]):
            return jsonify({"success": False, "message": "请提供完整的注册信息"}), 400

        if User.query.filter_by(username=username).first():
            return jsonify({"success": False, "message": "用户名已经存在"}), 400

        if password != repassword:
            return jsonify({"success": False, "message": "两次密码不一致"}), 409

        try:
            user = User(
                username=username,
                password=password,  # 自动哈希处理
                permissions=Permission.DATA_VIEW
            )
            db.session.add(user)
            db.session.commit()
            token=generate_jwt(user.to_dict())
           
            return jsonify({
                "success": True,
                "message": "注册成功",
                "user_id": user.id,
                "token": token
            }), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({"success": False, "message": f"注册失败: {str(e)}"}), 500

    # 处理GET请求
    return render_template('register.html')
from flask import g
@app.route('/auth')
@jwt_required
def auth():
    return jsonify({
        "success": True,
        "message": "已登录",
        "user_id": g.current_user,
        "code":200
    })
@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return jsonify({"success": True, "message": "已退出登录"})

@app.route('/user', methods=['GET', 'POST'])
@login_required
def get_current_user():
    return jsonify({
        "user": current_user.to_dict(),
        "permissions": current_user.permissions
    })
@app.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    if current_user.role != 'admin':
        abort(403)
    return render_template('admin.html')

@app.route('/water_quality', methods=['GET', 'POST'])
@permission_required(Permission.DATA_VIEW)
def water_quality():
    data = MonitorData.query.all()
    return jsonify([{
        'date': d.monitor_date.strftime('%Y-%m-%d'),
        'time': d.monitor_time.strftime('%H:%M:%S') if d.monitor_time else None,  # 新增时间字段
        'water_quality_class': d.water_quality_class,
        'temperature': d.temperature,
        'ph': d.ph,
        'dissolved_oxygen': d.dissolved_oxygen,
        'conductivity': d.conductivity,
        'turbidity': d.turbidity,
        'permanganate_index': d.permanganate_index,
        'ammonia_nitrogen': d.ammonia_nitrogen,
        'total_phosphorus': d.total_phosphorus,
        'total_nitrogen': d.total_nitrogen,
        'chlorophyll_alpha': d.chlorophyll_alpha,
        'algae_density': d.algae_density
    } for d in data])


# ------------ 鱼类数据接口 ------------
@app.route('/fish', methods=['GET', 'POST'])
@login_required
def fish_collection():
        fishes = Fish.query.all()
        return jsonify([{
            'id': fish.id,
            'species': fish.species,
            'weight': fish.weight,
            'length1': fish.length1,
            'length2': fish.length2,
            'length3': fish.length3,
            'height': fish.height,
            'width': fish.width
        } for fish in fishes])

@app.route('/weather', methods=['POST'])
def get_weather():
    # 从请求体获取JSON数据
    try:
        data = request.get_json()
        if not data:
            raise ValueError("Empty JSON data")

        lat = data.get('latitude')
        lon = data.get('longitude')
    except Exception as e:
        return jsonify({"error": "无效的JSON格式", "details": str(e)}), 400

    # 参数验证
    if None in (lat, lon):
        return jsonify({"error": "需要提供latitude和longitude参数"}), 400

    try:
        lat = float(lat)
        lon = float(lon)
        if not (-90 <= lat <= 90) or not (-180 <= lon <= 180):
            raise ValueError
    except ValueError:
        return jsonify({"error": "经纬度必须为有效数值（纬度：-90~90，经度：-180~180）"}), 400

    # 构造请求URL
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        weather_data = response.json()

        return jsonify({
            "coordinates": {"latitude": lat, "longitude": lon},
            "weather": weather_data['current_weather']
        })

    except requests.exceptions.Timeout:
        return jsonify({"error": "天气服务响应超时"}), 504
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "天气服务请求失败", "details": str(e)}), 502
    except KeyError:
        return jsonify({"error": "天气数据解析失败"}), 500
    except Exception as e:
        return jsonify({"error": "服务器内部错误", "details": str(e)}), 500
@app.context_processor
def inject_permissions():
    return dict(Permission=Permission)

if __name__ == '__main__':
    with app.app_context():
       init_db(db)
    app.run(debug=True)