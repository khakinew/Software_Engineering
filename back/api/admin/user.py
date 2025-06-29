from flask import Blueprint,jsonify,request
from models.models import permission_required,Permission,User,db
from werkzeug.security import generate_password_hash
from utils.utils import jwt_required
user=Blueprint('user',__name__,url_prefix="/admin/user")
@user.get("/get_user_list")
# @jwt_required
def get_user_list():
    dataList=[]
    data=User.query.all()
    for i in data:
        user=i.to_dict()
        user['status']="active" if user['status'] else "inactive"
        dataList.append(user)
    return jsonify(code=200,data=dataList)
@user.delete("/delete")
@jwt_required
def delete_user():
    userid=request.args.get("id")
    user=User.query.filter_by(id=userid).first()
    if user is None:
        return jsonify(code=400)
    if user.username=='admin':
        return jsonify(code=400)
    db.session.delete(user)
    db.session.commit()
    return jsonify(code=200)


@user.post("/add")
@jwt_required
def add_user():
    data=request.get_json()
    username=data.get("username")
    password=data.get("password")
    role=data.get("role")
    if username is None or password is None or role is None:
        return jsonify(code=400,message="请提供完整的用户信息")
    user=User.query.filter_by(username=username).first()
    if  user is not None:
        return jsonify(code=400,message="用户已存在")
    try:
        db.session.add(User(username=username,password=password,role=role))
        db.session.commit()
    except  Exception as e:
        db.session.rollback()
        return jsonify(code=500,message="失败")
    return jsonify(code=200)




@user.put("/edit")
@jwt_required
def edit_user():
    data=request.get_json()
    username=data.get("username")
    password=data.get("password")
    role=data.get("role")
    if username is None or password is None or role is None:
        return jsonify(code=400,message="请提供完整的用户信息")
    user=User.query.filter_by(username=username).first()
    if  user is  None:
        return jsonify(code=400,message="用户不存在")
    try:
      user.role=role
      user.username=username
      user.password=password
      db.session.commit()
    except  Exception as e:
        db.session.rollback()
        return jsonify(code=500,message="失败")
    return jsonify(code=200)