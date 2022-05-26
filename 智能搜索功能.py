# def 检索数据库：
#     if 存在该文字：
#         筛选出所有符合条件的数据
#         按照数量进行排序
#         显示前9条
#     else：
#         print("未找到该内容")
# IF 输入英文：
#     检索数据库
# ELIF 输入中文：compositionstart--compositionend
#     IF 拼写完成：
#         检索数据库
# 回传{key:keyword,value:activate}
from flask import Flask, render_template, request, jsonify
from settings import Config, db
from models import House
from sqlalchemy import func

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)


# 1、视图函数
@app.route('/')
def index():
    sum_num = House.query.count()
    # print(sum_num)#2、sqlalchemy获取房源数量
    house_new_list = House.query.order_by(House.publish_time.desc()).limit(6).all()
    house_hot_list = House.query.order_by(House.page_view.desc()).limit(4).all()
    # print(house_new_list)
    return render_template('index.html', num=sum_num, house_new_list1=house_new_list, house_hot_list1=house_hot_list)
    # return render_template('index.html',num=sum_num)#3、渲染


@app.route('/search/keyword/', methods=['POST'])
def search_kw():
    kw = request.form['kw']
    info = request.form['info']
    print("kw==" + kw)
    if info == '地区搜索':
        result = House.query.with_entities(House.address, func.count()).filter(House.address.contains(kw)).group_by(
            'address').order_by(func.count()).limit(9).all()[::-1]
        #                        print(result)
        if len(result) >= 1:
            #     for i in result:
            #         print(i)
            data = []
            for i in result:
                data.append({'t_name': i[0], 'num': i[1]})
            return jsonify({'code': 1, 'info': data})
        else:
            return jsonify({'code': 1, 'info':[]})
    if info == '户型搜索':
        result = House.query.with_entities(House.rooms, func.count()).filter(House.rooms.contains(kw)).group_by(
            'rooms').order_by(func.count()).limit(9).all()[::-1]
        # print(result)
        if len(result) >= 1:
            #     for i in result:
            #         print(i)
            data = []
            for i in result:
                data.append({'t_name': i[0], 'num': i[1]})
            return jsonify({'code': 1, 'info': data})
        else:
            return jsonify({'code': 1, 'info': []})
    return 'ok'
if __name__ == '__main__':
        app.run()
