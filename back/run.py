import csv
from io import StringIO

from flask import Flask, render_template, redirect, url_for, request, jsonify, abort, make_response
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
from api.alerts import alerts
app.register_blueprint(alerts)
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
# @permission_required(Permission.DATA_VIEW)
def water_quality():
    data = MonitorData.query.all()
    return jsonify([{
        'site':d.site_id,
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


@app.route('/getsite', methods=['GET', 'POST'])
# @permission_required(Permission.DATA_VIEW)
def get_site():
    data = Site.query.all()
    return jsonify([
        {
            'id': d.id,
            'province': d.province,
            'basin': d.basin,
            'site_name': d.site_name,
            'status': d.site_status
        } for d in data
    ])

@app.route('/merged_data', methods=['GET', 'POST'])
# @permission_required(Permission.DATA_VIEW)
def merged_data():
    try:
        water_quality_data = MonitorData.query.all()
        site_data = Site.query.all()

        site_dict = {site.id: site for site in site_data}
        merged = []
        for water in water_quality_data:
            site = site_dict.get(water.site_id)
            if site:
                merged.append({
                'site_id': water.site_id,
                'site_name': site.site_name,
                'province': site.province,
                'basin': site.basin,
                'status': site.site_status,
                'date': water.monitor_date.strftime('%Y-%m-%d'),
                'time': water.monitor_time.strftime('%H:%M:%S') if water.monitor_time else None,
                'water_quality_class': water.water_quality_class,
                'temperature': water.temperature,
                'ph': water.ph,
                'dissolved_oxygen': water.dissolved_oxygen,
                'conductivity': water.conductivity,
                'turbidity': water.turbidity,
                'permanganate_index': water.permanganate_index,
                'ammonia_nitrogen': water.ammonia_nitrogen,
                'total_phosphorus': water.total_phosphorus,
                'total_nitrogen': water.total_nitrogen,
                'chlorophyll_alpha': water.chlorophyll_alpha,
                'algae_density': water.algae_density
                })

        return jsonify(merged)
    except Exception as e:
        print("merged_data 接口错误：", str(e))
        return jsonify({"error": str(e)}), 500

# ------------ 鱼类数据接口 ------------
@app.route('/fish', methods=['GET', 'POST'])
# @login_required
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


# 在 run.py 中添加以下内容

@app.route('/monitor_data', methods=['GET'])
@jwt_required
def export_monitor_data():

    # 获取所有监测数据
    data = MonitorData.query.all()

    # 创建 CSV 字符串
    csv_output = StringIO()
    csv_writer = csv.writer(csv_output)

    # 写入表头
    headers = ['站点ID', '监测日期', '监测时间', '水质类别', '水温(℃)', 'pH', '溶解氧(mg/L)',
               '电导率(μS/cm)', '浊度(NTU)', '高锰酸盐指数(mg/L)', '氨氮(mg/L)',
               '总磷(mg/L)', '总氮(mg/L)', '叶绿素α(mg/L)', '藻密度(cells/L)']
    csv_writer.writerow(headers)

    # 写入数据行
    for d in data:
        csv_writer.writerow([
            d.site_id,
            d.monitor_date.strftime('%Y-%m-%d') if d.monitor_date else '',
            d.monitor_time.strftime('%H:%M:%S') if d.monitor_time else '',
            d.water_quality_class,
            d.temperature,
            d.ph,
            d.dissolved_oxygen,
            d.conductivity,
            d.turbidity,
            d.permanganate_index,
            d.ammonia_nitrogen,
            d.total_phosphorus,
            d.total_nitrogen,
            d.chlorophyll_alpha,
            d.algae_density
        ])

    # 创建响应对象
    output = make_response(csv_output.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=monitor_data.csv"
    output.headers["Content-type"] = "text/csv"
    return output


@app.route('/sites', methods=['GET'])
@jwt_required
def export_sites():
    sites = Site.query.all()

    csv_output = StringIO()
    csv_writer = csv.writer(csv_output)

    headers = ['站点ID', '省份', '流域', '站点名称', '站点状态']
    csv_writer.writerow(headers)

    for site in sites:
        csv_writer.writerow([
            site.id,
            site.province,
            site.basin,
            site.site_name,
            site.site_status
        ])

    output = make_response(csv_output.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=sites.csv"
    output.headers["Content-type"] = "text/csv"
    return output


# 在 run.py 中添加以下内容

@app.route('/import', methods=['POST'])
@jwt_required
def import_monitor_data():
    if 'file' not in request.files:
        return jsonify(success=False, message="没有文件"), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify(success=False, message="没有选择文件"), 400

    if not file.filename.endswith('.csv'):
        return jsonify(success=False, message="文件格式不正确"), 400

    try:
        # 读取 CSV 文件
        stream = StringIO(file.stream.read().decode("GBK"), newline=None)
        csv_reader = csv.reader(stream)
        next(csv_reader)  # 跳过表头

        for row in csv_reader:
            # 解析行数据
            if len(row) < 15:  # 检查列数
                continue

            monitor_data = MonitorData(
                site_id=int(row[0]),
                monitor_date=datetime.strptime(row[1], '%m/%d/%Y').date() if row[1] else None,                monitor_time=datetime.strptime(row[2], '%H:%M:%S').time() if row[2] else None,
                water_quality_class=row[3],
                temperature=float(row[4]) if row[4] else None,
                ph=float(row[5]) if row[5] else None,
                dissolved_oxygen=float(row[6]) if row[6] else None,
                conductivity=float(row[7]) if row[7] else None,
                turbidity=float(row[8]) if row[8] else None,
                permanganate_index=float(row[9]) if row[9] else None,
                ammonia_nitrogen=float(row[10]) if row[10] else None,
                total_phosphorus=float(row[11]) if row[11] else None,
                total_nitrogen=float(row[12]) if row[12] else None,
                chlorophyll_alpha=float(row[13]) if row[13] else None,
                algae_density=float(row[14]) if row[14] else None
            )
            db.session.add(monitor_data)

        db.session.commit()
        return jsonify(success=True, message="数据导入成功")

    except Exception as e:
        db.session.rollback()
        return jsonify(success=False, message=f"导入失败: {str(e)}"), 500


@app.route('/fish_export', methods=['GET'])
@jwt_required
def export_fish_data():
    # 获取所有鱼类数据
    fishes = Fish.query.all()

    # 创建 CSV 字符串
    csv_output = StringIO()
    csv_writer = csv.writer(csv_output)

    # 写入表头
    headers = ['ID', '物种', '重量(g)', '体长1(cm)', '体长2(cm)', '体长3(cm)', '高度(cm)', '宽度(cm)']
    csv_writer.writerow(headers)

    # 写入数据行
    for fish in fishes:
        csv_writer.writerow([
            fish.id,
            fish.species,
            fish.weight,
            fish.length1,
            fish.length2,
            fish.length3,
            fish.height,
            fish.width
        ])

    # 创建响应对象
    output = make_response(csv_output.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=fish_data.csv"
    output.headers["Content-type"] = "text/csv"
    return output


@app.route('/fish_stats', methods=['GET'])
@jwt_required
def get_fish_stats():
    try:
        # 获取不同鱼种数量
        species_count = db.session.query(db.func.count(db.distinct(Fish.species))).scalar()

        # 获取鱼的总数量
        total_fish = db.session.query(db.func.count(Fish.id)).scalar()

        # 计算平均重量
        avg_weight = db.session.query(db.func.avg(Fish.weight)).scalar() or 0

        return jsonify({
            "success": True,
            "species_count": species_count,
            "total_fish": total_fish,
            "avg_weight": round(avg_weight, 2)
        })
    except Exception as e:
        print(f"获取鱼类统计数据失败: {str(e)}")
        return jsonify({
            "success": False,
            "message": "获取鱼类统计数据失败",
            "error": str(e)
        }), 500


@app.route('/fish_metrics', methods=['GET'])
@jwt_required
def get_fish_metrics():
    try:
        # 获取不同鱼种数量
        species_count = db.session.query(db.func.count(db.distinct(Fish.species))).scalar()

        # 获取鱼的总数量
        total_fish = db.session.query(db.func.count(Fish.id)).scalar()

        # 计算平均重量
        avg_weight = db.session.query(db.func.avg(Fish.weight)).scalar() or 0

        # 计算平均体长（使用length1字段）
        avg_length = db.session.query(db.func.avg(Fish.length1)).scalar() or 0

        # 获取今日新增鱼的数量
        today = datetime.now().date()
        today_added = db.session.query(db.func.count(Fish.id)) \
                          .filter(Fish.created_at >= today) \
                          .scalar() or 0

        return jsonify({
            "success": True,
            "species_count": species_count,
            "total_fish": total_fish,
            "avg_weight": round(avg_weight, 1),
            "avg_length": round(avg_length, 1),
            "today_added": today_added
        })
    except Exception as e:
        print(f"获取鱼类指标失败: {str(e)}")
        return jsonify({
            "success": False,
            "message": "获取鱼类指标失败",
            "error": str(e)
        }), 500

@app.route('/fish_analysis', methods=['GET'])
@jwt_required
def fish_analysis():
    try:
        # 按照鱼种分组，统计每种鱼的平均重量、平均高度、平均长度和平均宽度
        analysis_data = db.session.query(
            Fish.species,
            db.func.avg(Fish.weight).label('avg_weight'),
            db.func.avg(Fish.height).label('avg_height'),
            db.func.avg(Fish.length1).label('avg_length'),  # 假设使用 length1 作为长度字段
            db.func.avg(Fish.width).label('avg_width')
        ).group_by(Fish.species).all()

        result = []
        for row in analysis_data:
            result.append({
                'species': row.species,
                'avg_weight': round(row.avg_weight, 2),
                'avg_height': round(row.avg_height, 2),
                'avg_length': round(row.avg_length, 2),
                'avg_width': round(row.avg_width, 2)
            })

        return jsonify({
            "success": True,
            "data": result
        })
    except Exception as e:
        print(f"获取鱼类分析数据失败: {str(e)}")
        return jsonify({
            "success": False,
            "message": "获取鱼类分析数据失败",
            "error": str(e)
        }), 500


@app.route('/province_site_count', methods=['GET'])
@jwt_required
def get_province_site_count():
    try:
        # 统计不同省份的站点数量
        province_site_count = db.session.query(Site.province, db.func.count(Site.id)).group_by(Site.province).all()

        result = []
        for province, count in province_site_count:
            result.append({
                'province': province,
                'site_count': count
            })

        # 返回统一格式的响应
        return jsonify({
            "success": True,
            "code": 200,
            "message": "获取成功",
            "data": result
        })
    except Exception as e:
        print(f"获取不同省份的站点数量失败: {str(e)}")
        return jsonify({
            "success": False,
            "code": 500,
            "message": "获取不同省份的站点数量失败",
            "error": str(e)
        }), 500

if __name__ == '__main__':
    with app.app_context():
       init_db(db)
    app.run(debug=True)