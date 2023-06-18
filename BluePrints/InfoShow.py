from flask import Blueprint, g, render_template, redirect, jsonify
from exts import db, cursor
from SQLModel import User, Vip, Res, Foods, Foods_Price, Orders, Orders_Detail
Infoshow = Blueprint("InfoShow", __name__, url_prefix="/ShowInfo")


@Infoshow.route("/<name>", methods=["POST", "GET"])
def data_show(name):
    if g.username == "admin":
        if name == 'user':
            datalist = User.query.all()
            # print(datalist)
            return render_template("4_user.html", datalist=datalist)
        elif name == 'vip':
            datalist = Vip.query.all()
            return render_template("5_vip.html", datalist=datalist)
        elif name == 'restaurant':
            datalist = Res.query.all()
            return render_template("6_Restaurant.html", datalist=datalist)
        elif name == 'foods':
            datalist = Foods.query.all()
            return render_template("7_foods.html", datalist=datalist)
        elif name == 'foods_price':
            datalist = Foods_Price.query.all()
            return render_template("8_foods_price.html", datalist=datalist)
        elif name == 'orders':
            datalist = Orders.query.all()
            return render_template("9_orders.html", datalist=datalist)
        elif name == 'orders_detail':
            datalist = Orders_Detail.query.all()
            return render_template("10_orders_detail.html", datalist=datalist)
        elif name == 'setting':
            return render_template('2_setting.html')
        elif name == 'user_log':
            cursor.commit()
            datalist = cursor.execute('select * from user_operate_logs')
            return render_template("5_user_log.html", datalist=datalist)
    elif g.username is None:
        return redirect("/login")
    else:
        return redirect("/")
