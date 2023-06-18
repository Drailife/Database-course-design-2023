# 放置表结构
from exts import db


class User(db.Model):  # 继承db对象
    __tablename__ = 'user'  # 表名
    usr_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    usr_name = db.Column(db.String(40), nullable=False)
    mail = db.Column(db.String(50), nullable=False)
    sex = db.Column(db.String(2), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    telephone = db.Column(db.String(50), nullable=False, unique=True)
    address_ = db.Column(db.String(200), nullable=False)
    password_ = db.Column(db.String(50), nullable=False)
    all_attr = ['usr_id', 'usr_name', 'mail', 'sex',
                'age', 'telephone', 'address_', 'password_']


class Vip(db.Model):
    __tablename__ = 'vip'
    vip_id = db.Column(db.Integer, db.ForeignKey(
        "user.usr_id"), primary_key=True)
    vip_level = db.Column(db.Integer, nullable=False, default=1)
    Subscription_time = db.Column(db.Date, nullable=False)
    validity_period = db.Column(db.Integer, nullable=False)


class Res(db.Model):
    __tablename__ = 'restaurant'
    res_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    res_name = db.Column(db.String(50), nullable=False)
    mail = db.Column(db.String(100), nullable=False)
    telephone = db.Column(db.String(15), nullable=False)
    address_ = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)


class Foods(db.Model):
    __tablename__ = 'foods'
    food_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    food_name = db.Column(db.String(100), nullable=False)
    kind = db.Column(db.Integer, nullable=False)


class Foods_Price(db.Model):
    __tablename__ = 'foods_price'
    food_id = db.Column(db.Integer, db.ForeignKey(
        "foods.food_id"), primary_key=True)
    res_id = db.Column(db.Integer, db.ForeignKey(
        "restaurant.res_id"), primary_key=True, nullable=False)
    price = db.Column(db.Float)
    description_ = db.Column(db.String(200))


class Orders(db.Model):
    __tablename__ = 'orders'
    order_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    usr_id = db.Column(db.Integer, db.ForeignKey(
        "user.usr_id"), nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    actual_price = db.Column(db.Float, nullable=False)
    time_ = db.Column(db.DateTime, nullable=False)


class Orders_Detail(db.Model):
    __tablename__ = 'orders_detail'
    order_id = db.Column(db.Integer, db.ForeignKey(
        "orders.order_id"), primary_key=True)
    res_id = db.Column(db.Integer, db.ForeignKey(
        "foods_price.res_id"), primary_key=True)
    food_id = db.Column(db.Integer, db.ForeignKey(
        "foods_price.food_id"), primary_key=True)
    num = db.Column(db.Integer, nullable=False)
