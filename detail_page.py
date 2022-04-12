from flask import Blueprint, render_template, jsonify, request
from models import House, User, Tuijian
from sqlalchemy import func
# # from utils.regression_data import linear_model_main
# # from settings import db
# # from utils.pearson_tuijian import recommed

detail_page = Blueprint('detail_page', __name__)

# 实现房源的基本信息展示
"""
1. 创建一个视图函数 动态路由 /house/<int:hid> method=get
2. 使用房源编号 通过sqlalchemy获取编号对应的房源对象 就可以获取对象中的信息了
3. 使用render_template进行模板的渲染
"""
@detail_page.route('/house/<int:hid>')
def detail(hid):
    house=House.query.get(hid)
    return render_template('detail_page.html',house=house)
    sheshi_str = house.sheshi  # 床-宽带-洗衣机-空调-热水器-暖气
    sheshi_list = sheshi_str.split('-')
# 可以添加价格走势，户型占比，房源数量，户型价格走势，推荐房源





# 过滤器--用来实现 交通字段 无数据的时候 显示 暂无数据！
def deal_traffic_txt(word):
    if len(word) == 0 or word is None:
        return '暂无数据！'
    else:
        return word


detail_page.add_app_template_filter(deal_traffic_txt, 'dealNone')
