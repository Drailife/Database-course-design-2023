import json
from flask_sqlalchemy import SQLAlchemy
from flask import Blueprint, Flask, render_template, request, session, redirect, g
from exts import db
from SQLModel import User
from BluePrints.InfoShow import Infoshow
from BluePrints.Login import Login
from BluePrints.Update import Update
from BluePrints.Res_Operate import Res_show
from BluePrints.User_Operate import User_Operate
from flask_migrate import Migrate

import config
# print(Flask.__doc__)

app = Flask(__name__)
# 绑定配置文件
app.config.from_object(config)

db.init_app(app)
migrate = Migrate(app, db)
# ORM模型映射成表的三步
# 1. flask db init 只需要执行一次
# 2. flask db migrate 识别ORM模型的改变，生成迁移脚本
# 3. flask db upgrade 运行迁移脚本，同步到数据库中
app.register_blueprint(Infoshow)  # 蓝图绑定
app.register_blueprint(Login)

app.register_blueprint(Update)
app.register_blueprint(Res_show)
app.register_blueprint(User_Operate)


@app.route("/")
def index():
    infoToHtml = session.get('username', default=None)
    return render_template("1_index.html", data=infoToHtml)


@app.before_request
def my_before_request():
    # if session.get('id', default=None) is None:
    #     return redirect('/'login)
    username = session.get("username", default=None)  # 用户名字，即@前的数据
    type = session.get("type", None)  # 用户类型，即admin user res三种
    g.username = username
    g.type = type


@app.context_processor
def my_context_processor():
    return {"user": g.username, "type": g.type}


if __name__ == '__main__':
    app.run(debug=True)
