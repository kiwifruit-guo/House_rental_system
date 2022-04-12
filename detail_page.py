from flask import Blueprint, render_template, jsonify, request
from models import House, User, Tuijian
from utils.connect_to_database import query_data
from settings import db
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
4. 展示一次页面自动使得浏览量加一
"""
#添加浏览记录
# 登陆状态下：cookie-name-浏览记录：
#     已经存在浏览记录：
#         hid在浏览记录中：
#             pass
#         else:
#             添加hid，返回房源详情
#     else:
#         插入hid，返回房源详情

@detail_page.route('/house/<int:hid>')
def detail(hid):
    house = House.query.get(hid)
    liulangliang = house.liulanliang
    id = str(house.id)
    # sql_list = ['use beijing_house_data;', f'update soufang set liulanliang=liulanliang+1 where id={id}']
    # for sql in sql_list:
    #     result = query_data(sql)
    house.liulanliang+=1
    db.session.commit()
    sheshi_str = house.sheshi  # 床-宽带-洗衣机-空调-热水器-暖气
    sheshi_list = sheshi_str.split('-')

    name=request.cookies.get('name')
    if name:
        user=User.query.filter(User.name==name).first()
        seen_id_str=user.seen_id
        # print(seen_id_str)
        if seen_id_str:
            seen_id_list=seen_id_str.split(',')
            set_id=set([int(i) for i in seen_id_list])
            if hid in set_id:
                pass
            else:
                user.seen_id=seen_id_str+str(hid)
                db.session.commit()

        else:
            user.seen_id=str(hid)
            db.session.commit()
    return render_template('detail_page.html', house=house,sheshi=sheshi_list)



# 可以添加价格走势，户型占比，房源数量，户型价格走势，推荐房源



# 过滤器--用来实现 交通字段 无数据的时候 显示 暂无数据！
def deal_traffic_txt(word):
    if len(word) == 0 or word is None:
        return '暂无数据！'
    else:
        return word


detail_page.add_app_template_filter(deal_traffic_txt, 'dealNone')
