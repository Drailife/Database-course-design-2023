# 该文件用于定义用户点餐的蓝图
from flask import Blueprint, g, render_template, redirect, session, request
from exts import cursor, conn
from SQLModel import Res, Foods_Price, Foods
Res_show = Blueprint("res_show", __name__, url_prefix="/res_operate")

# 餐厅基本食品信息的展示
res_infos = [i for i in range(0, 10)]

cursor = conn.cursor()


@Res_show.route("/my_restaurant", methods=["POST", "GET"])
def my_restaurant():
    mail = session.get('mail', default=None)  # 通过邮件来获取餐厅的所有菜品数据
    if mail is None:
        return redirect('/login')
    print('res_id---:', session['id'])
    res_name = cursor.execute(
        'select res_name from restaurant where res_id="%s"' % (session['id'])).fetchone()[0]
    # 通过视图来获取需要传递给html的信息
    datas = cursor.execute(
        'select * from ALL_FOODS_INFO where res_name="%s"' % (res_name)).fetchall()
    for data in datas:
        print('---------', data)

    # 获取菜品的具体星系
    # 根据res_id在食品-餐厅表中查询该餐厅的所有食物
    return render_template("11_my_restaurant.html", datas=datas, res_name=res_name, res_id=session['id'], res_infos=res_infos, menu_id='1')

# 订单展示


@Res_show.route('/myres_orders', methods=["POST", "GET"])
def myres_orders():
    res_name = cursor.execute('select res_name from restaurant where res_id = "%s"' % (
        session['id'])).fetchone()[0]
    datas = cursor.execute(
        'select * from Orders_Detail_By_Usr_Id where res_name="%s"' % (res_name)).fetchall()
    return render_template("11_my_restaurant.html", menu_id='2', data_orders_detail=datas, res_infos=res_infos)

# 餐厅信息


@Res_show.route('/myres_info', methods=["POST", "GET"])
def myres_info():
    res_infos = cursor.execute(
        "select * from restaurant where res_id = '%s'" % (session['id'])).fetchone()
    return render_template("11_my_restaurant.html", res_infos=res_infos, menu_id='3')


@Res_show.route("/edit_foods", methods=["POST", "GET"])
def edit_foods():
    dataToHtml = "数据已更新"
    datas = dict(request.form)
    cursor.execute(
        'select food_id from foods where food_name="%s"' % (datas['food_name']))
    foodTablehaveThisFood = cursor.fetchone()
    if foodTablehaveThisFood is not None:  # 表示修改的食品存在于foods表中
        print('在表foods中', foodTablehaveThisFood)
    else:
        print('不在表foods中')
        # 需要先插入到foods中然后再更改
        cursor.execute('insert into foods value(null,"%s","1")' %
                       (datas['food_name']))
    food_id_ = cursor.execute(
        'select food_id from foods where food_name="%s"' % (datas['food_name'])).fetchone()[0]
    try:
        cursor.execute('''update foods_price set food_id ="%s",price="%s",description_="%s"
        where food_id="%s" and res_id="%s"''' % (food_id_, datas['price'],
                                                 datas['desc'], datas['food_id'], session['id']))
    except Exception as e:
        cursor.rollback()
        dataToHtml = f'Error: {e}'
    print(dataToHtml)
    cursor.commit()
    return dataToHtml


@Res_show.route("/add_foods", methods=["POST", "GET"])
def add_foods():
    dataToHtml = 'success'
    dataforms = dict(request.form)
    print(dataforms)
    if not (len(dataforms['food_name']) and len(dataforms['desc'])):
        return "信息输入不完整"
    cursor.execute('''select count(*) from foods_price fp, foods f
    where fp.food_id =f.food_id and res_id="%s" and food_name="%s"''' % (session['id'], dataforms['food_name']))
    repeta_food = cursor.fetchone()[0]
    if (repeta_food == 1):
        return "餐厅中已经存在该商品，无法添加"
    # 开始添加商品 先检查food表中是否有该食物
    cursor.execute(
        'select food_id from foods where food_name="%s"' % (dataforms['food_name']))
    foodTablehaveThisFood = cursor.fetchone()
    try:
        if foodTablehaveThisFood is not None:  # 表示修改的食品存在于foods表中
            print('在表foods中', foodTablehaveThisFood)
            foodTablehaveThisFood = foodTablehaveThisFood[0]
        else:
            print('不在表foods中')
            # 需要先插入到foods中然后再插入到foods_price表中g
            cursor.execute('insert into foods value(null,"%s","1")' %
                           (dataforms['food_name']))
            foodTablehaveThisFood = cursor.execute(
                "select LAST_INSERT_ID()").fetchone()[0]
            print('---', foodTablehaveThisFood)

        cursor.execute('insert into foods_price value("%s","%s","%s","%s")' % (
            foodTablehaveThisFood, session['id'], dataforms['price'], dataforms['desc']))
    except Exception as e:
        cursor.rollback()
        dataToHtml = f'添加失败{e}'
    cursor.commit()
    return dataToHtml


@Res_show.route("/del_foods", methods=["POST", "GET"])
def del_foods():
    datas = dict(request.form)
    print(datas)
    try:
        cursor.execute('delete from foods_price where food_id="%s" and res_id="%s"' % (
            datas['food_id'], session['id']))
        cursor.commit()
        return "success"
    except Exception as e:
        cursor.rollback()
        cursor.commit()
        print(e)
        return f"Error:{e}"

# 商家信息界面的信息修改


@Res_show.route("/eitd_res_infos", methods=["POST", "GET"])
def eitd_res_infos():
    datas = dict(request.form)
    print(datas)
    try:
        cursor.execute(
            '''update restaurant set res_name='%s',mail='%s',telephone='%s',\
            address_='%s',password="%s" where res_id="%s"''' % (datas['res_name'], datas['mail'],
                                                                datas['tel'], datas['address'], datas['password'], datas['res_id']))
    except Exception as e:
        cursor.rollback()
        return f"Error: {e}"
    cursor.commit()
    return 'success'
