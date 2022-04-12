from flask import Blueprint, request, Response, jsonify, render_template, redirect
from models import User, House
from settings import db
import json

user_page = Blueprint('user_page', __name__)

# 实现注册功能
"""
1. 创建一个视图函数 /register POST请求方式
2. 获取用户的注册信息 昵称 密码 邮箱
3. 校验用户昵称是否已经存在
    3.1 昵称已经存在了 ==> 用户已经注册过这个用户名了 ==> 返回提示信息 告诉用户这个名字 你不能使用
    3.2 昵称不存在    ==> 用户名为使用过           ==> 保存用户信息  然后跳转到用户中心页 再设置cookie
"""


@user_page.route('/register', methods=["POST"])
def register():
    # 获取用户的注册信息 昵称 密码 邮箱
    name = request.form['username']
    password = request.form['password']
    email = request.form['email']

    # 查询使用已经有用户注册
    result = User.query.filter(User.name == name).all()

    # 判断用户是否已经注册 如果没有注册 在返回的结果中 设置cookie
    if len(result) == 0:
        user = User(name=name, password=password, email=email)
        db.session.add(user)
        db.session.commit()
        print(user, '注册成功')

        # {'valid': '1','msg': 成功==>用户名  失败==>'注册失败！'}
        json_str = json.dumps({'valid': '1', 'msg': user.name})

        res = Response(json_str)  # 实例化的过程中  需要给他传入响应内容
        res.set_cookie('name', user.name, 3600 * 2)  # key value 过期时间 单位秒

        return res

    # 用户名已经被注册过
    else:

        return jsonify({'valid': '0', 'msg': '注册失败！'})


# 实现用户中心页
"""
1. 创建一个视图函数 /user/<name> get请求方式
2. 获取name字段的值 根据这个值 查询用户表  获取用户对象

   如果获取到这个用户对象
   2.1 提取用户对象user中的信息  
   2.2 获取collect_id  和 seen_id  ==>  根据id获取房源对象
   2.3 使用render_template进行渲染

   如果没有获取到这个对象
   2.4 使用重定向  定向到首页   
"""


@user_page.route('/user/<name>')
def user(name):
    # 查询用户表  获取用户对象
    # first 获取结果的时候 如果有结果  就返回第一个结果 如果没有结果 就直接返回None
    # all   获取结果的时候 如果有结果  返回符合条件的所有结果 放在一个列表中  如果没有结果 就直接返回空列表
    user = User.query.filter(User.name == name).first()

    # 判断用户存在
    if user.name==request.cookies.get('name'):

        # 获取用户的收藏记录 collect_id  存储格式：'123，234，345'  如果用户没有收藏记录 null
        collect_id_str = user.collect_id

        if collect_id_str:
            # 从collect_id中获取 每一个房源的id
            collect_id_list = collect_id_str.split(',')  # '123，234，345'  ==> ['123','234','345']

            collect_house_list = []
            # 根据房源的id  使用sqlalchemy获取房源对象
            for hid in collect_id_list:
                house = House.query.get(int(hid))

                # 将 房源对象 放到列表中
                collect_house_list.append(house)
        else:
            collect_house_list = []

        # 获取用户的浏览记录 seen_id 存储格式：'123，234，345'  如果用户没有收藏记录 null
        seen_id_str = user.seen_id

        if seen_id_str:

            # 从seen_id中获取 每一个房源的id
            seen_id_list = seen_id_str.split(',')

            seen_house_list = []
            # 根据房源的id  使用sqlalchemy获取房源对象
            for hid in seen_id_list:
                house = House.query.get(int(hid))

                seen_house_list.append(house)
        else:
            seen_house_list = []

        return render_template('user_page.html', user=user, collect_house_list=collect_house_list,
                               seen_house_list=seen_house_list)

    # 如果用户不存在  使用重定向 将页面跳转到首页
    elif user.name!=request.cookies.get('name') or not request.cookies.get('name'):
        return redirect('/')

    else:
        return redirect('/')  # redirct作用实现重定向 需要给他传入一个路径作为参数  这个路径必须是视图函数中使用到的路径


# 实现登陆功能
"""
1. 创建一个视图函数 /login POST请求方式
2. 首先需要获取用户提交的信息 用户的名字和密码
3. 进行校验 先根据用户的名字 来进行校验
   一、用户存在
      继续验证密码 是否和这个用户对象保存的密码一致
      如果密码正确：{'valid':'1', 'msg':name}  并保存登陆状态
      如果密码不对：{'valid':'0', 'msg':'密码不正确！'}

   二、用户不存在   
      直接返回结果：{'valid':'0', 'msg':'用户名不正确'}
"""


@user_page.route('/login', methods=['POST'])
def login():
    # 首先需要获取用户提交的信息 用户的名字和密码
    name = request.form['username']
    password = request.form['password']

    # 根据用户的名字 来进行校验
    user = User.query.filter(User.name == name).first()

    # 用户存在
    if user:
        # 密码也正确
        if user.password == password:
            # 将响应信息变化成json字符串
            result = {'valid': '1', 'msg': user.name}
            result_json = json.dumps(result)
            # 放入响应内容
            res = Response(result_json)
            # 设置登陆状态
            res.set_cookie('name', user.name, 3600 * 2)
            return res

        else:
            return jsonify({'valid': '0', 'msg': '密码不正确！'})

    # 用户不存在的时候
    else:
        return jsonify({'valid': '0', 'msg': '用户名不正确！'})


# 实现退出登录的功能
"""
1. 创建一个视图函数 /logout  get请求方式
2. 首先 检查浏览器中是否有cookie存在
   如果能够从cookie中取到name的值  就代表cookie存在 也代表用户处于登录状态
      处于登录状态下，我们就删除用户的cookie，然后重定向到首页

   如果不能从cookie中取到name的值  就代表cookie不存在  也就代表用户处于非登录状态下
      处于非登录状态下，直接返回json信息
"""


@user_page.route('/logout')
def logout():
    # 检查浏览器中是否有cookie存在
    name = request.cookies.get('name')

    # 代表用户处于登录状态
    if name:
        result = {'valid': '1', 'msg': '退出登录成功！'}
        json_str = json.dumps(result)
        res = Response(json_str)
        # 删除用户的cookie
        res.delete_cookie('name')  # 需要传入一个参数 用来指定删除那条cookie

        return res

    # 代表用户处于非登录状态下
    else:
        return jsonify({'valid': '0', 'msg': '未登录！'})


# 实现用户修改信息的功能
"""
1. 创建一个视图函数 /modify/userinfo/<option> POST请求方式
2. 首先 我们需要获取路由中携带的这个option参数 通过这个参数 获取用户要修改的字段
3. 通过request对象 获取用户的名字  和 要修改的字段的新值
4. 判断用户是否存在  根据用户提交的名字来判断的
    如果 这个用户存在的话，更新新值 并返回json字符串  {'ok':'1'}
    如果 这个用户不存在的话  直接返回json字符串 {'ok':'0'}
"""


@user_page.route('/modify/userinfo/<option>', methods=['POST'])
def mofity_info(option):
    if option == 'name':
        # 用户的原来名字
        y_name = request.form['y_name']
        # 用户的新的名字
        name = request.form['name']

        # 查询用户是否存在
        user = User.query.filter(User.name == y_name).first()

        # 用户存在
        if user:
            # 更新新的名字
            user.name = name
            db.session.commit()

            # 组装json字符串
            result = {'ok': '1'}
            json_str = json.dumps(result)
            # 创建响应对象
            res = Response(json_str)
            res.set_cookie('name', user.name, 3600 * 2)

            return res

        # 用户不存在
        else:
            return jsonify({'ok': '0'})

    elif option == 'addr':
        # 获取用户的名字
        y_name = request.form['y_name']
        # 获取新的地址
        addr = request.form['addr']

        # 查询用户是否存在
        user = User.query.filter(User.name == y_name).first()

        # 用户存在
        if user:
            # 更新新的地址
            user.addr = addr
            db.session.commit()

            # 返回json字符串
            return jsonify({'ok': '1'})

        # 用户不存在
        else:
            return jsonify({'ok': '0'})


    elif option == 'password':
        # 获取用户的名字
        y_name = request.form['y_name']
        # 获取新的密码
        password = request.form['password']

        # 查询用户是否存在
        user = User.query.filter(User.name == y_name).first()

        # 用户存在
        if user:
            # 更新新的地址
            user.password = password
            db.session.commit()

            # 返回json字符串
            return jsonify({'ok': '1'})

        # 用户不存在
        else:
            return jsonify({'ok': '0'})

    elif option == 'email':
        # 获取用户的名字
        y_name = request.form['y_name']
        # 获取新的email
        email = request.form['email']

        # 查询用户是否存在
        user = User.query.filter(User.name == y_name).first()

        # 用户存在
        if user:
            # 更新新的地址
            user.email = email
            db.session.commit()

            # 返回json字符串
            return jsonify({'ok': '1'})

        # 用户不存在
        else:
            return jsonify({'ok': '0'})

    return 'ok'


# 实现收藏房源的功能
"""
1. 创建一个视图函数 /add/collection/<int:hid>  get请求方式：
2. 获取房源hid
3. 判断用户是否处于登录状态下 使用浏览器中保存的cookie来进行判断
    用户处于登录状态下：
        可以从cookie中获取用户的name字段的值 根据这个值 获取用户对象
        从用户对象中  获取collect_id这个字段 格式：'123，234，345'  或者 null
            如果存在 收藏记录
                '123，234，345'  ==> ['123','234','345']
                对列表进行过滤获取没有重复的房源id
                判断 当前hid 是否处于 这个列表中
                    如果处于这个列表中 返回json字符串 告诉用户 已经收藏过了
                    如果未处于这个列表中  需要将hid 插入到列表中  然后在更新 数据中收藏的字段 返回用户 告诉他 收藏完成了

            如果 没有收藏记录 null
                直接将hid插入到数据库中 返回用户 收藏成功    

    用户没有处于登录状态下：
        直接返回json字符串 告诉用户 需要登录后才能使用收藏功能
"""


@user_page.route('/add/collection/<int:hid>')
def add_collection_id(hid):
    # 判断用户是否处于登录状态下
    name = request.cookies.get('name')

    # 用户处于登录状态下
    if name:
        # 获取用户对象
        user = User.query.filter(User.name == name).first()
        # 从用户对象中  获取collect_id这个字段
        collect_id_str = user.collect_id

        # 收藏记录存在的情况
        if collect_id_str:
            # '123，234，345'  ==> ['123','234','345']
            collect_id_list = collect_id_str.split(',')

            # 对列表进行过滤获取没有重复的房源id  ['123','234','345'] ==> [123,234,345]
            # 使用set函数对列表中的数据进行过滤 获取没有重复id的集合
            set_id = set([int(i) for i in collect_id_list])

            if hid in set_id:
                return jsonify({'valid': '1', 'msg': '已经收藏过了!'})

            # 代表为收藏的过程
            else:
                new_collect_id_str = collect_id_str + ',' + str(hid)
                # 修改数据库中的信息
                user.collect_id = new_collect_id_str
                db.session.commit()
                return jsonify({'valid': '1', 'msg': '收藏完成!'})

        # 收藏记录为null的情况
        else:
            user.collect_id = str(hid)
            db.session.commit()

            return jsonify({'valid': '1', 'msg': '收藏完成!'})

    # 用户处于未登录状态下
    else:
        return jsonify({'valid': '0', 'msg': '需要登录后才能使用收藏功能'})


# 使用取消收藏的功能
"""
1. 创建一个视图函数 /collect_off  POST请求方式
2. 从前端提交的数据中  获取name字段和房源的id  根据name字段的值 获取用户对象
3. 从用户对象中 获取collect_id字段  不需要进行判断的 直接过去收藏记录
4. 判断房源id是否在 collect_house_id中
    有这个id   删除此id  然后把删除后结果重新保存到数据库中
    如果没有这个id  直接返回json  告知用户 删除失败
"""


@user_page.route('/collect_off', methods=['POST'])
def collect_off():
    # 从前端提交的数据中  获取name字段和房源的id
    name = request.form['user_name']
    hid = request.form['house_id']

    # 根据name字段的值 获取用户对象
    user = User.query.filter(User.name == name).first()

    # 从用户对象中 获取collect_id字段
    collect_id_str = user.collect_id  # 数据格式示例：'123,234,345'
    collect_id_list = collect_id_str.split(',')  # '123,234,345' ==> ['123', '234', '345']

    # 存在于收藏记录中
    if hid in collect_id_list:
        # 删除 收藏房源的id
        collect_id_list.remove(hid)  # 示例：假如要删除'123'这个房源  ['123', '234', '345'] ==> ['234', '345']

        # 将删除后的结果 重新变换成字符串 保存到数据库中  list ==> str
        new_collect_id_str = ','.join(collect_id_list)  # ['234', '345']  ==> '234,345'

        user.collect_id = new_collect_id_str
        db.session.commit()

        result = {'valid': '1', 'msg': '删除成功！'}
        return jsonify(result)

    else:
        result = {'valid': '0', 'msg': '删除失败！'}
        return jsonify(result)


# 实现删除浏览记录的功能
"""
1. 创建一个视图函数  /del_record  POST请求方式
2. 从前端获取发送过来的 用户名  ， 根据用户名 获取用户对象，然后获取对象的浏览记录
3. 判断浏览记录存在与否 
    如果存在的 清空浏览记录  
    如果不存在 什么都不做
    {'valid':'1', 'msg':'删除成功'}
"""


@user_page.route('/del_record', methods=['POST'])
def del_record():
    # 获取前端传递过来的用户名
    name = request.form['user_name']

    # 获取用户对象
    user = User.query.filter(User.name == name).first()

    # 获取对象的浏览记录
    seen_id_str = user.seen_id

    # 浏览记录存在的时候
    if seen_id_str:
        user.seen_id = ''
        db.session.commit()

        return jsonify({'valid': '1', 'msg': '删除成功!'})

    # 浏览记录不存在的时候
    else:
        return jsonify({'valid': '0', 'msg': '暂无信息可以删除!'})











