from flask import Blueprint, g, render_template, redirect, session, request
from exts import db
from SQLModel import User, Res
Login = Blueprint("Login", __name__, url_prefix="/login")


@Login.route("/", methods=["POST", "GET"])
def login():
    # 我是笨比，只能这么改了
    return redirect('/')


@Login.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# 进入到用户或者管理员主页面


@Login.route("/<usr_name>", methods=["POST", "GET"])
def main_show_info(usr_name):
    data = request.form
    print(data)
    usr_mail = data.get('mail')  # 获得邮箱地址
    print(usr_mail)
    usr_cur = User.query.filter_by(mail=usr_mail).first()
    print(usr_cur)
    if usr_cur is None:
        return "用户名不存在"
    else:
        session['id'] = usr_cur.usr_id
        usr_password = usr_cur.password_
        print(usr_password)
    usr_name = usr_mail[:usr_mail.find('@')]
    session['username'] = usr_name  # 设置整体的usrname
    # 登录管理员界面
    if data.get('password') != usr_password:
        return '密码错误！'
    elif usr_name == "admin" and data.get("password") == usr_password:
        session['type'] = 'admin'  # 用来标识用户的类型
    else:  # 普通点餐用户
        session['type'] = 'user'
        session['mail'] = usr_mail
    return redirect("/")


# 进入到商家界面
@Login.route("/res", methods=["POST", "GET"])
def res_show_info():
    data = dict(request.form)
    print(data)
    mail = data.get('mail')  # 获得邮箱地址
    print(mail)
    res_cur = Res.query.filter_by(mail=mail).first()

    print(res_cur)
    if res_cur is None:
        return "用户名不存在"
    else:
        password = res_cur.password
        session['id'] = res_cur.res_id
        print(password)
    res_name = mail[:mail.find('@')]
    session['username'] = res_name  # 设置整体的usrname
    session['type'] = 'res'
    session['mail'] = mail
    if data.get('password') != password:
        return '密码错误！'
    return "success"
