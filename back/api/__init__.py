from flask import Blueprint
from .admin.user import user as user_blueprint
api=Blueprint('api',__name__,url_prefix='/api')
api.register_blueprint(user_blueprint,)