
# 后端检查满足要求的所有房源
# 渲染列表页
from flask import Flask,Blueprint, render_template, request, jsonify
from models import House
from models import House
from sqlalchemy import func

# 使用Blueprint类初识化的到一个对象  蓝图的名字 包的名字
index_page = Blueprint('index_page', __name__)

@index_page.route('/')
def index():
    # 获取全部房源数量功能
    house_total_num = House.query.count()

    # 获取最新房源top6的功能
    # House.query.order_by('publish_time')
    house_new_list = House.query.order_by(House.publish_time.desc()).limit(6).all()

    # 获取最热房源top4的功能
    # House.query.order_by('liulanliang')
    house_hot_list = House.query.order_by(House.page_view.desc()).limit(4).all()
    # print(house_hot_list)

    return render_template('index.html', num=house_total_num,
                           house_new_list1=house_new_list,
                           house_hot_list1=house_hot_list)  # template_name 用来接收一个模板文件的名字的  context 需要接收模板文件用到的变量




@index_page.route('/search/keyword/', methods=['POST'])
def search_kw():
    # 1. 获取前端传递过来的查询参数 kw：查询关键字 info：查询字段
    kw = request.form['kw']
    info = request.form['info']

    # 2. 根据查询参数  过滤房源信息
    # 2.1 info：查询字段 分两种情况 地区搜索 户型搜索
    if info == '地区搜索':
        # 当info 等于 地区搜索的时候  去过滤address这个字段
        result = House.query.with_entities(House.address, func.count()).filter(House.address.contains(kw)).group_by(
            'address').order_by(func.count().desc()).limit(9).all()

        if len(result):  # 使用len获取result结果的长度 如果有结果 长度 大于等于1  如果没有结果 长度 等于0
            data = []
            for i in result:
                data.append({'t_name': i[0], 'num': i[1]})
            return jsonify({'code': 1, 'info': data})
        else:

            return jsonify({'code': 0, 'info': []})

    if info == '户型搜索':
        result = House.query.with_entities(House.rooms, func.count()).filter(House.rooms.contains(kw)).group_by(
            'rooms').order_by(func.count().desc()).limit(9).all()
        if len(result):  # 使用len获取result结果的长度 如果有结果 长度 大于等于1  如果没有结果 长度 等于0
            data = []
            for i in result:
                data.append({'t_name': i[0], 'num': i[1]})
            return jsonify({'code': 1, 'info': data})
        else:

            return jsonify({'code': 0, 'info': []})

# 将这个对象注册到app中
