
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_login import (
    LoginManager,
    UserMixin,
    login_required,
    current_user,
)
from functools import wraps
login_manager = LoginManager()
login_manager.login_view = 'login'
db=SQLAlchemy()
class Permission:
    DATA_VIEW = 0x01    # 查看数据权限 (00000001)
    DATA_EDIT = 0x02    # 编辑数据权限 (00000010)
    USER_MANAGE = 0x04  # 用户管理权限 (00000100)
    SITE_MANAGE = 0x08  # 站点管理权限 (00001000)
    ADMIN = 0x80        # 管理员权限 (10000000)
    DATA_IMPORT_EXPORT = 0x10  # 数据导入导出权限 (00010000)
class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password_hash = db.Column(db.String(100))
    role = db.Column(db.String(20), default='user')
    permissions = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    create_time=db.Column(db.DateTime, default=datetime.now())
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
            "permissions": self.permissions,
            "status": self.is_active,
            "createTime": self.create_time.strftime("%Y-%m-%d %H:%M:%S")
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

    def __init__(self, **kwargs):
        super(MonitorData, self).__init__(**kwargs)
        # 设置默认值或验证逻辑
        if not self.monitor_date:
            self.monitor_date = datetime.now().date()


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

def init_db(db):
    db.create_all()
    if not User.query.filter_by(username='admin').first():
        admin = User(username='admin', role='admin')
        admin.password = 'admin123'  
        db.session.add(admin)
        db.session.commit()