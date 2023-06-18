# 该文件用于定义用户点餐的蓝图
import os
from flask import Blueprint, g, render_template, redirect, session, request
from exts import cursor, conn
User_Operate = Blueprint("User_operate", __name__, url_prefix="/user_operate")

# 餐厅基本食品信息的展示

# 展示商品页面

usrdata = [i for i in range(20)]


@User_Operate.route("/purchase", methods=["POST", "GET"])
def purchase():
    # 从定义的视图中获取数据
    cursor.execute(
        "select * from `foods_available_for_purchase` order by res_name")
    datas = cursor.fetchall()
    print(datas)
    return render_template("12_User_Purchase_From_Res.html", dataForPurchase=datas, menu_id='1', user_infos=usrdata)

# 用户添加商品到购物车


@User_Operate.route("/add_to_shopcart", methods=["POST", "GET"])
def addtoshopcart():
    datas = dict(request.form)
    print(f"用户id: {session['id']}  ", datas)
    cursor.execute("CALL `ADDTOSHOPCART`('%s', '%s', '%s', '%s');" % (
        session['id'], datas['res_name'], datas['food_name'], datas['price']))
    print(cursor.fetchall())
    cursor.execute('select 1')
    cursor.commit()  # 提交
    return '成功添加到购物车'

# 购物车页面展示


@User_Operate.route("/shopping_cart", methods=["POST", "GET"])
def shop():
    cursor.execute(
        "select res_name,food_name,num,total_price from `shopping_cart` order by res_name")
    datas = cursor.fetchall()
    cursor.execute(
        "select sum(total_price) from `shopping_cart` where usr_id='%s'" % (session['id']))
    prices = cursor.fetchone()[0]
    return render_template("12_User_Purchase_From_Res.html", shopping_cart_info=datas, menu_id='2',
                           total_price=prices, user_infos=usrdata)
# 实现购物车减少数据的功能


@User_Operate.route("/sub_from_shopcart", methods=["POST", "GET"])
def sub_from_shopcart():
    datas = dict(request.form)
    print(datas)
    if (int(datas['num']) > 1):  # 若num>1则数量减一 否者删除
        cursor.execute(
            '''UPDATE shopping_cart SET num = num - 1
            WHERE usr_id='%s' AND res_name='%s'
            AND food_name='%s\'''' % (session['id'], datas['res_name'], datas['food_name']))
    else:
        cursor.execute('''DELETE FROM SHOPPING_CART
        WHERE usr_id='%s' AND res_name='%s'
        AND food_name='%s\'''' % (session['id'], datas['res_name'], datas['food_name']))
    cursor.commit()
    cursor.execute(
        "select sum(total_price) from `shopping_cart` where usr_id='%s'" % (session['id']))
    price = cursor.fetchone()[0]
    return str(price)  # 返回的是购物车的总价值

# 实现购物车清空或者购买的操作


@User_Operate.route("/shopcurt/<operate>", methods=["POST", "GET"])
def cls_or_purchase(operate):
    if operate == 'cls':
        cursor.execute(
            'delete from SHOPPING_CART where usr_id="%s"' % (session['id']))
        cursor.commit()
    elif (operate == 'purchase'):
        datas = dict(request.form)
        if datas['total_price'] == 'None':
            return '购物车为空'
        print(float(datas['total_price']))
        # 调用存储过程添加数据到orders
        cursor.execute(
            "call PURCHASE_FROM_SHOPPING_CURT('%s','%s','%s')" % (
                session['id'], datas['total_price'], datas['total_price']))
        # 添加数据到orders_detail中
        order_id = cursor.execute('select LAST_INSERT_ID()').fetchone()[0]
        # 获取当前用户的购物车
        cursor.execute(
            "select * from `shopping_cart` where usr_id='%s'" % (session['id']))
        shopping_curt_info = cursor.fetchall()  # 购物车数据
        for items in shopping_curt_info:  # 点击提交后将购物车数据添加到orders_detail中
            res_id = cursor.execute(
                "select res_id from restaurant where res_name = '%s'" % (items[1])).fetchone()[0]
            food_id = cursor.execute(
                "select food_id from foods where food_name = '%s'" % (items[2])).fetchone()[0]
            print(
                f'order_id: {order_id} res_id : {res_id} food_id : {food_id}')
            # 插入到订单细则中
            cursor.execute(
                '''insert into orders_detail value('%s','%s','%s','%s')''' % (order_id, res_id, food_id, items[3]))
        # 提交订单后清空购物车
        cursor.execute(
            'delete from SHOPPING_CART where usr_id="%s"' % (session['id']))
        cursor.commit()
        return '下单成功!'
    return 'success'


@User_Operate.route("/my_orders", methods=["POST", "GET"])
def orders_show():
    cursor.execute('''select order_id,total_price,actual_price,time_ 
    from Orders where usr_id="%s"''' % (session['id']))
    cursor.commit()
    data_orders = cursor.fetchall()
    print(data_orders)
    return render_template('12_User_Purchase_From_Res.html', data_orders=data_orders, menu_id='3', user_infos=usrdata)


@User_Operate.route("/my_orders_details", methods=["POST", "GET"])
def orders_details():
    usr_name = cursor.execute(
        'select usr_name from user where usr_id="%s"' % (session['id'])).fetchone()[0]
    # 从视图中获得需要传递给前端的数据
    cursor.execute(
        'select * from Orders_Detail_By_Usr_Id where usr_name = "%s"' % (usr_name))
    datas = cursor.fetchall()
    print(datas)
    return render_template('12_User_Purchase_From_Res.html', menu_id='4',
                           data_orders_detail=datas, user_infos=usrdata)

# 展示个人信息


@User_Operate.route("/user_infos", methods=["POST", "GET"])
def user_infos_show():
    usrdata = cursor.execute(
        'select * from user where usr_id="%s"' % (session['id'])).fetchall()[0]
    print('----', usrdata)
    return render_template('12_User_Purchase_From_Res.html', menu_id='5', user_infos=usrdata)

# 修改个人信息


@User_Operate.route("/edit_user", methods=["POST", "GET"])
def user_edit():
    datas = dict(request.form)
    print('*****', datas)
    try:
        cursor.execute('''update user set usr_name='%s',mail="%s",sex="%s",age="%s",
        telephone="%s",address_="%s",password_="%s" 
        where usr_id="%s"''' % (datas['usr_name'], datas['mail'],
                                datas['sex'], datas['age'], datas['telephone'],
                                datas['address_'], datas['password_'], datas['usr_id']))
    except Exception as e:
        cursor.rollback()
        return f'Error:{e}'
    cursor.commit()
    return 'success'


BackFIleName = './SqlFIle/backup.sql'

path = os.getcwd()


@User_Operate.route("/backup", methods=["POST", "GET"])
def backup():
    print('backup')
    os.system('mysqldump -uroot -pawsl --all-databases > "%s"' %
              (os.path.join(path, BackFIleName)))
    return '数据库已备份\n备份地址:\n %s' % (os.path.join(path, BackFIleName))


@User_Operate.route("/recover", methods=["POST", "GET"])
def recover():
    print(path)
    os.system(f'"{path}\\static\\2.exe"')
    cursor.commit()
    return '数据库已恢复'
