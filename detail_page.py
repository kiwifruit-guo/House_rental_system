from flask import Blueprint, render_template, jsonify, request
from models import House, User, Tuijian
from utils.connect_to_database import query_data
from settings import db
from sqlalchemy import func
#
# # # from utils.regression_data import linear_model_main
# # # from settings import db
# # # from utils.pearson_tuijian import recommed
#
# detail_page = Blueprint('detail_page', __name__)
#
# # 实现房源的基本信息展示
# """
# 1. 创建一个视图函数 动态路由 /house/<int:hid> method=get
# 2. 使用房源编号 通过sqlalchemy获取编号对应的房源对象 就可以获取对象中的信息了
# 3. 使用render_template进行模板的渲染
# 4. 展示一次页面自动使得浏览量加一
# """
# #添加浏览记录
# # 登陆状态下：cookie-name-浏览记录：
# #     已经存在浏览记录：
# #         hid在浏览记录中：
# #             pass
# #         else:
# #             添加hid，返回房源详情
# #     else:
# #         插入hid，返回房源详情
#
# @detail_page.route('/house/<int:hid>')
# def detail(hid):
#     house = House.query.get(hid)
#     page_view = house.page_view
#     id = str(house.id)
#     # sql_list = ['use beijing_house_data;', f'update soufang set liulanliang=liulanliang+1 where id={id}']
#     # for sql in sql_list:
#     #     result = query_data(sql)
#     house.page_view+=1
#     db.session.commit()
#     sheshi_str = house.sheshi  # 床-宽带-洗衣机-空调-热水器-暖气
#     sheshi_list = sheshi_str.split('-')
#
#     name=request.cookies.get('name')
#     if name:
#         user=User.query.filter(User.name==name).first()
#         seen_id_str=user.seen_id
#         # print(seen_id_str)
#         if seen_id_str:
#             seen_id_list=seen_id_str.split(',')
#             set_id=set([int(i) for i in seen_id_list])
#             if hid in set_id:
#                 pass
#             else:
#                 user.seen_id=seen_id_str+str(hid)
#                 db.session.commit()
#
#         else:
#             user.seen_id=str(hid)
#             db.session.commit()
#     return render_template('detail_page.html', house=house,sheshi=sheshi_list)
#
#
#
# # 可以添加价格走势，户型占比，房源数量，户型价格走势，推荐房源
#
#
#
# # 过滤器--用来实现 交通字段 无数据的时候 显示 暂无数据！
# def deal_traffic_txt(word):
#     if len(word) == 0 or word is None:
#         return '暂无数据！'
#     else:
#         return word
#
#
# detail_page.add_app_template_filter(deal_traffic_txt, 'dealNone')

from flask import Blueprint, render_template, jsonify, request
from models import House, User, Tuijian
from sqlalchemy import func
from utils.regression_data import linear_model_main
from settings import db


detail_page = Blueprint('detail_page', __name__)

# 实现房源的基本信息展示
"""
1. 创建一个视图函数 动态路由 /house/<int:hid> method=get
2. 使用房源编号 通过sqlalchemy获取编号对应的房源对象 就可以获取对象中的信息了
3. 使用render_template进行模板的渲染
"""

# 实现添加浏览记录的功能
"""
1. 判断用户是否处于登录状态下 通过cookie来判断是否处于登录状态下
2. 在登陆状态下
    通过cookie来获取用户的name值， 通过这个name值 获取用户对象， 获取用户对象的浏览记录
        已经存在的浏览记录
            判断当前的hid 是否在浏览记录中
                如果hid在浏览记录中 什么也不做 直接返回房源详情信息
                如果hid不在浏览记录中 首先将hid添加到当前的浏览记录中  然后更新数据库  然后返回房源的详情信息
        浏览记录为null
            直接将当前的hid插入到浏览记录中 然后更新数据库 然后返回房源信息

3. 没有在登陆状态下
        直接返回当前房源的详情信息
"""

# 实现推荐房源的功能
"""
1. 在登陆状态下
    1.1 添加用户的浏览次数
        第一种情况，该用户对此房源已经浏览过了，就对推荐表中score进行加一
        第二种情况，该用户对此房源没有浏览过，直接插入一条新的数据
    1.2 根据推荐系统的返回值，给用户返回推荐结果
        第一种情况，有推荐的返回值，就代表有推荐房源，此时返回推荐房源给用户
        第二种情况，没有推荐的返回值，代表推荐房源为空列表，此时返回同小区的房源给用户
2. 非登录状态下
    2.1 返回同小区的房源
"""


def recommed(id):
    pass


@detail_page.route('/house/<int:hid>')
def detail(hid):
    house = House.query.get(hid)
    page_view = house.page_view
    id = str(house.id)
    # sql_list = ['use beijing_house_data;', f'update soufang set liulanliang=liulanliang+1 where id={id}']
    # for sql in sql_list:
    #     result = query_data(sql)
    house.page_view+=1
    db.session.commit()
    sheshi_str = house.sheshi  # 床-宽带-洗衣机-空调-热水器-暖气
    sheshi_list = sheshi_str.split('-')

    # 判断用户是否处于登录状态下
    name = request.cookies.get('name')

    # 定义一个用来盛放推荐房源的列表容器
    tuijian = []

    # 在登陆状态下
    if name:
        # 获取用户对象
        user = User.query.filter(User.name == name).first()

        # 获取用户对象的浏览记录
        seen_id_str = user.seen_id  # 浏览记录的格式：'123，234，345' 或着 null

        # 已经存在的浏览记录
        if seen_id_str:

            # 对浏览记录进行变形 将字符串 转换成 列表 '123，234，345' ==> ['123','234','345']
            seen_id_list = seen_id_str.split(',')

            # 将列表转换成 元素为整数的列表 ['123','234','345'] ==> [123, 234, 345]
            # 借助set函数 来去重
            set_id = set([int(i) for i in seen_id_list])  # [123, 234, 345] ==> {123, 234,345}

            # 如果hid在浏览记录中
            if hid in set_id:
                pass

            # 如果hid不在浏览记录中
            else:
                new_seen_id_str = seen_id_str + ',' + str(hid)
                user.seen_id = new_seen_id_str
                db.session.commit()

        # 浏览记录为null
        else:
            # 直接将当前的hid插入到浏览记录中
            user.seen_id = str(hid)
            db.session.commit()

        # TODO 实现推荐功能
        # 添加用户的浏览次数
        # 查询 tuijian表中是否有当前用户 对此房源的浏览记录
        info = Tuijian.query.filter(Tuijian.user_id == user.id, Tuijian.house_id == house.id).first()

        # 第一种情况，该用户对此房源已经浏览过了，就对推荐表中score进行加一
        if info:
            print('推荐表中已经存在<user:{}>对<house:{}>的浏览记录'.format(user.id, house.id))
            new_score = info.score + 1
            info.score = new_score
            db.session.commit()
            print('完成：对<user:{}><house:{}>浏览记录+1的操作'.format(user.id, house.id))


        # 第二种情况，该用户对此房源没有浏览过，直接插入一条新的数据
        else:
            new_info = Tuijian(user_id=user.id, house_id=house.id, title=house.title, address=house.address,
                               block=house.block, score=1)
            db.session.add(new_info)
            db.session.commit()
            print('推荐表中不存在<user:{}>对<house:{}>的浏览记录，因此添加一条新的信息到推荐表中'.format(user.id, house.id))

        # 根据推荐系统的返回值，给用户返回推荐结果
        # 调用推荐系统的recommed函数
        result = recommed(user.id)

        # 第一种情况，有推荐的返回值，就代表有推荐房源，此时返回推荐房源给用户
        if result:
            print('-----使用推荐系统，获取推荐房源给用户-----')
            for tuijian_hid, tuijian_num in result:
                tuijian_house = House.query.get(int(tuijian_hid))
                tuijian.append(tuijian_house)

        # 第二种情况，没有推荐的返回值，代表推荐房源为空列表，此时返回同小区的房源给用户
        else:
            print('-----使用普通推荐系统，获取同小区的房源给用户-----')
            putong_tuijian = House.query.filter(House.address == house.address).order_by(House.page_view.desc()).all()

            if len(putong_tuijian) > 6:
                tuijian = putong_tuijian[:6]
            else:
                tuijian = putong_tuijian


    # 没有在登陆状态下
    else:
        print('-----使用普通推荐系统，获取同小区的房源给用户-----')
        putong_tuijian = House.query.filter(House.address == house.address).order_by(House.page_view.desc()).all()

        if len(putong_tuijian) > 6:
            tuijian = putong_tuijian[:6]
        else:
            tuijian = putong_tuijian

    return render_template('detail_page.html', house=house, sheshi=sheshi_list, tuijian=tuijian)


# 实现户型占比功能
"""
1. 创建一个视图函数 /get/piedata/<block> get请求方式
2. 获取block字段 使用sqlalchemy来查询符合block字段的房源
3. 分组统计房源中的户型 和 数量  根据数量对 户型进行排序 降序排序
4. 封装数据 
5. 提交给echarts
"""


@detail_page.route('/get/piedata/<block>')
def return_pie_data(block):
    print(block)
    # 1. 选择 filter(House.block == block)
    # 2. 预处理 group_by(House.rooms).order_by(func.count().desc())
    # 3. 预处理的结果是 result
    result = House.query.with_entities(House.rooms, func.count()).filter(House.block == block).group_by(
        House.rooms).order_by(func.count().desc()).all()

    # 4. 对数据进行变换 result ==> {'name': one_house[0], 'value': one_house[1]}
    data = []
    for one_house in result:
        data.append({'name': one_house[0], 'value': one_house[1]})
    return jsonify({'data': data})


# 实现本地区小区数量TOP20功能
"""
1. 创建一个视图函数 /get/columndata/<block> get请求方式
2. 获取block字段 使用sqlalchemy获取符合这个block字段的所有房源数据 --- 目标数据
3. 预处理 对目标数据 进行分组 依据小区名字进行分组 统计每个小区的房源数量  就可以根据房源数量 对小区进项排序 降序排序的方式————预处理的结果
4. 进行数据的变换 变换成能够提交给echarts的数据格式
5. 使用jsonify返回数据给前端
"""


@detail_page.route('/get/columndata/<block>')
def return_bar_data(block):
    result = House.query.with_entities(House.address, func.count()).filter(House.block == block).group_by(
        House.address).order_by(func.count().desc()).all()  # 小区名字出现在address这个字段中

    # {'name_list_x':['xxx小区','xxx小区','xxx小区'],'num_list_y':[160,149,128]}
    name_list = []
    num_list = []
    for addr, num in result:
        # 顺义-顺义城-西辛南区 ==> ['顺义-顺义城', '西辛南区'] ==> 西辛南区
        xiaoqu_name = addr.rsplit('-', 1)[1]
        name_list.append(xiaoqu_name)
        num_list.append(num)
    # 获取TOP20的数据 大于20的就直接舍去
    if len(name_list) > 20:
        data = {'name_list_x': name_list[:20], 'num_list_y': num_list[:20]}

    else:
        data = {'name_list_x': name_list, 'num_list_y': num_list}

    return jsonify({'data': data})


# 实现房价预测功能
"""
1. 创建一个视图函数 /get/scaterdata/<block> get请求方式
2. 获取block字段 然后使用sqlalchemy获取符合blocl字段的所有房源 --- 目标数据
3. 预处理 对目标数据进行分组 分组的依据就是房源的发布时间 使用func中avg()获取 price/area价格 按照发布时间进行排序  --- 预处理的结果
4. 对预处理的结果进行变换 得到能够提交给echarts的数据格式  {'data':[[0,50],[1,16.87],[2,76.49]]}
"""


@detail_page.route('/get/scatterdata/<block>')
def return_scatter_data(block):
    # 1. 实现已有数据的渲染
    result = House.query.with_entities(func.avg(House.price / House.area)).filter(House.block == block).group_by(
        House.publish_time).order_by(House.publish_time).all()
    data = []
    X = []
    Y = []
    for index, i in enumerate(result):
        X.append([index])
        Y.append(round(i[0], 2))
        data.append([index, round(i[0], 2)])  # round函数 可以完成浮点数的四舍五入的运算 传入两个参数 第一参数：浮点数 第二参数：保留的小数位

    # 2. 对未来一天（第二天）的价格进行预测
    predict_value = len(data)

    predict_outcome = linear_model_main(X, Y, predict_value)
    print(predict_outcome)
    p_outcome = round(predict_outcome[0], 2)

    # 3. 将预测的数据添加入data中
    data.append([predict_value, p_outcome])

    return jsonify({'data': data})


# 实现户型价格走势
"""
1. 创建一个视图函数 /get/brokenlinedata/<block> get请求方式
2. 获取block字段 使用sqlalchemy获取符合block字段 和 户型的房源数据 --- 目标数据
3. 预处理 对目标数据 进行分组 分组的依据是房源的发布时间 使用func函数中avg()获取 price/area价格 按照发布时间来进行排序 默认方式进行排序  --- 预处理的结果
4. 对预处理的结果 进行变换 的到 提供给echarts的数据  {'data':{'1室1厅':[76.49, 42.86]}}
"""


@detail_page.route('/get/brokenlinedata/<block>')
def return_brokenline_data(block):
    # 1室1厅的户型
    result = House.query.with_entities(func.avg(House.price / House.area)).filter(House.block == block,
                                                                                  House.rooms == '1室1厅').group_by(
        House.publish_time).order_by(House.publish_time).all()
    data = []
    for i in result[-14:]:
        data.append(round(i[0], 2))

    # 2室1厅的户型
    result1 = House.query.with_entities(func.avg(House.price / House.area)).filter(House.block == block,
                                                                                   House.rooms == '2室1厅').group_by(
        House.publish_time).order_by(House.publish_time).all()
    data1 = []
    for i in result1[-14:]:
        data1.append(round(i[0], 2))

    # 2室2厅的户型
    result2 = House.query.with_entities(func.avg(House.price / House.area)).filter(House.block == block,
                                                                                   House.rooms == '2室2厅').group_by(
        House.publish_time).order_by(House.publish_time).all()
    data2 = []
    for i in result2[-14:]:
        data2.append(round(i[0], 2))

    # 3室2厅的户型
    result3 = House.query.with_entities(func.avg(House.price / House.area)).filter(House.block == block,
                                                                                   House.rooms == '3室2厅').group_by(
        House.publish_time).order_by(House.publish_time).all()
    data3 = []
    for i in result3[-14:]:
        data3.append(round(i[0], 2))

    return jsonify({'data': {'1室1厅': data, '2室1厅': data1, '2室2厅': data2, '3室2厅': data3}})


# 过滤器--用来实现 交通字段 无数据的时候 显示 暂无数据！
def deal_traffic_txt(word):
    if len(word) == 0 or word is None:
        return '暂无数据！'
    else:
        return word


detail_page.add_app_template_filter(deal_traffic_txt, 'dealNone')
