from typing import Dict
from datetime import datetime as date
from config import Config
from functools import wraps
from flask import request, jsonify, g

import jwt
import datetime
def generate_jwt(payload: Dict, expire_minutes: int = 30) -> str:
    payload = payload.copy()
    # 使用 datetime.utcnow() 替代 date.utcnow()
    expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=expire_minutes)
    payload["exp"] = expire
    # 使用正确的 jwt.encode 方法
    token = jwt.encode(payload, Config.SECRET_KEY, algorithm=Config.ALGORITHM)
    return token

# ✅ 解码 JWT
def decode_jwt(token: str) -> Dict:
    """
    解码 JWT Token
    :param token: JWT 字符串
    :return: JSON 数据字典
    """
    try:
        decoded = jwt.decode(token, Config.SECRET_KEY, algorithms=[Config.ALGORITHM])
        return {"success": True, "data": decoded}
    except jwt.ExpiredSignatureError:
        return {"success": False, "message": "Token 已过期"}
    except jwt.InvalidTokenError:
        return {"success": False, "message": "无效的 Token"}

def jwt_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization', '')

        if not auth_header.startswith('Bearer '):
            return jsonify(success=False, message="缺少或无效的 Authorization Header",code=401), 401
        token = auth_header.split(' ')[1]

        try:
            payload =decode_jwt(token)
            g.current_user = payload
        except jwt.ExpiredSignatureError:
            return jsonify(success=False, message="Token 已过期",code=401), 401
        except jwt.InvalidTokenError:
            return jsonify(success=False, message="无效的 Token",code=401), 401

        return f(*args, **kwargs)
    return decorated_function