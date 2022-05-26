#最新房源和最热房源的展示通过@list_page.route('/list/pattern/<int:page>')实现，list_page
#搜索结果展示@list_page.route('/query') 实现，sousuo_page
from flask import Blueprint, request, render_template
from models import House

# 创建蓝图对象
list_page = Blueprint('list_page', __name__)

"""
实现搜索列表页的功能
1. 定义一个路由为 /query的视图函数
2. 使用request 获取到请求字段 具体的查询信息
3. 使用sqlalchemy 在字段中 查询具体的信息 获取满足这个条件的房源
4. 使用publish_time字段，进行降序排序
5. 使用render_template进行渲染
"""

#在这里可以增加分页功能
@list_page.route('/query')  # http://127.0.0.1:5000/query?request.args
def search_txt_info():
    # 获取地区字段的查询
    if request.args.get('addr'):
        addr = request.args.get('addr')
        result = House.query.filter(House.address == addr).order_by(House.publish_time.desc()).all()
        #print(result)
        return render_template('sousuo_list.html', house_list=result)

    # 获取户型字段的查询
    if request.args.get('rooms'):
        rooms_info = request.args.get('rooms')
        result = House.query.filter(House.rooms == rooms_info).order_by(House.publish_time.desc()).all()
        return render_template('sousuo_list.html', house_list=result)


# 获取最新房源列表页的功能
"""
1. 去定义一个视图函数 /list/pattern/<int:page>  method=get
2. 获取全部的房源数据，再根据房源的发布时间 publish_time 字段进行降序排序
3. 实现分页功能 借助分页插件 和 paginate函数来完成
4. 使用render_template进行渲染
"""


@list_page.route('/list/pattern/<int:page>')
def return_new_list(page):
    # 对列表的数据进行保护，只能查看前10页的数据，当请求的页码数大于10 或者页码数 小于0的时候，我们返回page=1
    if page > 10 or page <= 0:
        page =1
    result = House.query.order_by(House.publish_time.desc()).paginate(page, per_page=10)  # page 当前的页码数 per_page 每页所展示的数据条数
                                                                                           # paginate()函数 能够终止链式查询 作用和all（）相同

    return render_template('list.html', house_list=result.items, page_num=result.page)


# 获取最热房源列表页的功能
"""
1. 去定义一个视图函数 /list/pattern1/<int:page>  method=get
2. 获取全部的房源数据，再根据房源的浏览量 liulanliang 字段进行降序排序
3. 实现分页功能 借助分页插件 和 paginate函数来完成
4. 使用render_template进行渲染
"""


@list_page.route('/list/pattern1/<int:page>')
def return_hot_list(page):
    if page > 10 or page <= 0:
        page=1
    result = House.query.order_by(House.page_view.desc()).paginate(page, per_page=10)
    #return (result)
    return render_template('list.html', house_list=result.items, page_num=result.page)


# 实现过滤器 完成title字段的长度截取
def deal_title_over(word):
    if len(word) > 15:
        return word[:15] + '...'
    else:
        return word


# 字段无数据的情况下，显示暂无数据
def deal_direction(word):
    if len(word) == 0 or word is None:
        return '暂无信息！'
    else:
        return word


list_page.add_app_template_filter(deal_title_over, 'dealover')  # 第一个参数就是 函数的名字， 第二个参数就是 过滤器名字
list_page.add_app_template_filter(deal_direction, 'dealdirection')
