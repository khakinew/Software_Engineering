from flask import Flask, render_template, redirect, url_for, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    logout_user,
    login_required,
    current_user,
)
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import requests

# ------------ 初始化应用 ------------
app = Flask(__name__)
CORS(app, supports_credentials=True)  # 允许跨域带凭证
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///marine.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 初始化扩展
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# ------------ 定义模型 ------------
# 新增权限常量类
class Permission:
    DATA_VIEW = 0x01    # 查看数据权限 (00000001)
    DATA_EDIT = 0x02    # 编辑数据权限 (00000010)
    USER_MANAGE = 0x04  # 用户管理权限 (00000100)
    SITE_MANAGE = 0x08  # 站点管理权限 (00001000)
    ADMIN = 0x80        # 管理员权限 (10000000)


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password_hash = db.Column(db.String(100))
    role = db.Column(db.String(20), default='user')
    permissions = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role == 'admin':
            self.permissions = Permission.ADMIN | Permission.DATA_VIEW | Permission.DATA_EDIT | Permission.USER_MANAGE | Permission.SITE_MANAGE

    @property
    def password(self):
        raise AttributeError('密码不可读')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def has_permission(self, perm):
        return (self.permissions & perm) == perm

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "role": self.role,
            "permissions": self.permissions
        }

class Site(db.Model):
    __tablename__ = 'site'
    id = db.Column(db.Integer, primary_key=True)
    province = db.Column(db.String(50))
    basin = db.Column(db.String(50))
    site_name = db.Column(db.String(100))
    site_status = db.Column(db.String(50))

class MonitorData(db.Model):
    __tablename__ = 'monitor_data'
    id = db.Column(db.Integer, primary_key=True)
    site_id = db.Column(db.Integer, db.ForeignKey('site.id'))
    monitor_date = db.Column(db.Date)  # 日期字段（YYYY-MM-DD）
    monitor_time = db.Column(db.Time)  # 时间字段（HH:MM:SS）<-- 新增字段
    water_quality_class = db.Column(db.String(20))          # 水质类别
    temperature = db.Column(db.Float)                       # 水温(℃)
    ph = db.Column(db.Float)                                # pH(无量纲)
    dissolved_oxygen = db.Column(db.Float)                  # 溶解氧(mg/L)
    conductivity = db.Column(db.Float)                      # 电导率(μS/cm)
    turbidity = db.Column(db.Float)                         # 浊度(NTU)
    permanganate_index = db.Column(db.Float)                # 高锰酸盐指数(mg/L)
    ammonia_nitrogen = db.Column(db.Float)                  # 氨氮(mg/L)
    total_phosphorus = db.Column(db.Float)                  # 总磷(mg/L)
    total_nitrogen = db.Column(db.Float)                    # 总氮(mg/L)
    chlorophyll_alpha = db.Column(db.Float)                 # 叶绿素α(mg/L)
    algae_density = db.Column(db.Float)                     # 藻密度(cells/L)



class Fish(db.Model):
    __tablename__ = 'fish'
    id = db.Column(db.Integer, primary_key=True)
    species = db.Column(db.String(50))        # 鱼类名称
    weight = db.Column(db.Float)              # 重量（克）
    length1 = db.Column(db.Float)             # 长度1（厘米）
    length2 = db.Column(db.Float)             # 长度2（厘米）
    length3 = db.Column(db.Float)             # 长度3（厘米）
    height = db.Column(db.Float)              # 高度（厘米）
    width = db.Column(db.Float)               # 宽度（厘米）

# ------------ 权限装饰器 ------------
def permission_required(perm):
    def decorator(f):
        @wraps(f)
        @login_required
        def decorated_function(*args, **kwargs):
            if not current_user.has_permission(perm):
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def admin_required(f):
    return permission_required(Permission.ADMIN)(f)

# ------------ 用户加载器 ------------
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ------------ 所有路由 ------------
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
        # 强制解析JSON数据，忽略Content-Type
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
            return jsonify({
                "success": True,
                "user": user.to_dict(),
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
            return jsonify({
                "success": True,
                "message": "注册成功",
                "user_id": user.id
            }), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({"success": False, "message": f"注册失败: {str(e)}"}), 500

    # 处理GET请求
    return render_template('register.html')

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


@app.errorhandler(400)
def bad_request(e):
    return jsonify(success=False, message="请求参数错误"), 400

@app.errorhandler(401)
def unauthorized(e):
    return jsonify(success=False, message="未授权访问"), 401

@app.errorhandler(403)
def forbidden(e):
    return jsonify(success=False, message="禁止访问"), 403

@app.errorhandler(404)
def not_found(e):
    return jsonify(success=False, message="资源不存在"), 404

@app.errorhandler(500)
def internal_error(e):
    return jsonify(success=False, message="服务器内部错误"), 500

import requests

# ------------ 初始化函数 ------------
def create_initial_roles():
    if not User.query.filter_by(username='admin').first():
        admin = User(
            username='admin',
            password=generate_password_hash('admin123'),
            role='admin'
        )
        db.session.add(admin)
        db.session.commit()


# ------------ 模板上下文注入 ------------
@app.context_processor
def inject_permissions():
    return dict(Permission=Permission)

# ------------ 启动应用 ------------
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # 初始化管理员（密码自动哈希）
        if not User.query.filter_by(username='admin').first():
            admin = User(username='admin', role='admin')
            admin.password = 'admin123'  # 调用password setter
            db.session.add(admin)
            db.session.commit()
    app.run(debug=True)