from flask import Blueprint, request, jsonify, json
from SQLModel import User, Res, Vip, Orders, Orders_Detail, Foods, Foods_Price
from exts import db, dic, cursor

Update = Blueprint("Update", __name__, url_prefix="/update")
dic['res'] = Res
dic['user'] = User
dic['vip'] = Vip
dic['orders'] = Orders
dic['orders_detail'] = Orders_Detail
dic['foods'] = Foods
dic['foods_price'] = Foods_Price


@Update.route("/delete/<type>/<id>", methods=['GET', 'POST'])
def delete(type, id):
    item_id = request.form['item_id']
    if request.method == 'POST':
        if type == 'orders_detail':  # 处理组合主键问题
            item_id_2 = request.form['item_id_2']
            item_id_3 = request.form['item_id_3']
            data = dic[type].query.get((item_id, item_id_2, item_id_3))
            # cursor.execute('delete from %s where')
        elif type == 'foods_price':  # 处理组合主键问题
            item_id_2 = request.form['item_id_2']
            data = dic[type].query.get((item_id, item_id_2))
        else:
            data = dic[type].query.get(item_id)  # 查询是否有该条数据
            print(data.__dict__)
        if data:
            try:
                db.session.delete(data)  # 删除数据
                db.session.commit()  # 进行提交
                json_data = jsonify({'result': 'Delete Success!'})
            except Exception as e:
                db.session.rollback()
                print(f"删除出错{e}")
                json_data = jsonify({'result': f'Delete Error!\n报错:{e}'})
        else:
            json_data = jsonify({'result': '不存在该数据！'})
        db.session.commit()  # 进行提交
        return json_data  # 给前端返回处理后数据

# User添加用户


@Update.route("/add/user", methods=['POST', 'GET'])
def add_user():
    data = dict(request.form)
    print("--------------data form--------------")
    try:
        cursor.execute("insert into user value\
                                    (null,'%s','%s','%s','%s','%s','%s','%s')" %
                       (data['usr_name'], data['mail'], data['sex'], data['age'],
                        data['telephone'], data['address_'], data['password_']
                        ))
        '''提交任务到数据库中'''
        return_data = 'Add Success!'
        print(return_data)
    except Exception as e:
        cursor.rollback()
        print(f'Add error:\n\n {str(e)}')
        return_data = f'Add error:\n\n {str(e)}'
    cursor.commit()
    return return_data
# User查询


@Update.route("/query/user", methods=['POST', 'GET'])
def query_user():
    data_return = {'Success': 'Y'}
    data = dict(request.form)
    print(data)
    dic = {}
    for (key, value) in data.items():  # 去除返回的空数据
        if len(value) > 0:
            dic[key] = value
    # print('-----------dic', dic)
    info = User.query.filter_by(**dic).all()

    if len(info) != 0:
        for id, item in enumerate(info, 1):
            dic = {}
            for i in range(len(User.all_attr)):
                dic[User.all_attr[i]] = getattr(item, User.all_attr[i])
            data_return[f'data{id}'] = dic
        # data_return.append(dic)
        data_return = json.dumps(data_return)  # 返回给前端数据
        print(data_return)
        return data_return
    else:
        return jsonify({'Success': 'N'})
# res注册


@Update.route("/add/res", methods=['POST', 'GET'])
def add_res():
    data = dict(request.form)
    # 准备添加数据
    try:
        cursor.execute("""insert into restaurant value(null,"%s","%s","%s","%s","%s")""" % (
            data['res_name'],
            data['mail'],
            data['telephone'],
            data['address_'],
            data['password_']
        ))
        cursor.commit()
        return f'''商家注册成功!\n\n账号: {data["mail"]}\n密码: {data["password_"]}'''
    except Exception as e:
        cursor.rollback()
        cursor.commit()
        return f"注册失败!!\n报错:{e}"

# 使用ODBC更改密码


@Update.route("/reset_password", methods=['POST', 'GET'])
def reset_password():
    datainfo = dict(request.form)
    print(f"表单数据：{datainfo}")
    try:
        # 首先判断用户是否存在
        data = cursor.execute(
            f"select * from user where usr_id = {datainfo['usr_id']}").fetchall()
        print(data)
        if len(data) < 1:
            return f'USER ID为{datainfo["usr_id"]}的用户不存在'
        # 更改密码
        cursor.execute(
            f"CALL reset_password(\'{datainfo['usr_id']}\', \'{datainfo['password']}\');")
        cursor.commit()  # 提交
    except Exception as e:
        cursor.rollback()
        return f'Error:无法重置\nError{e}'
    return f"Usr Id为{datainfo['usr_id']}的用户密码已经重置\n"
