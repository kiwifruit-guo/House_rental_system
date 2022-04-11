from flask import Flask,render_template
from settings import Config,db
from models import House
app=Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
#1、视图函数
@app.route('/')
def index():
      sum_num=House.query.count()
      #print(sum_num)#2、sqlalchemy获取房源数量
      house_new_list = House.query.orderby(House.publish_time.desc()).limit(6).all()
      print(house_new_list)
      return render_template('index.html',num=sum_num)#3、渲染



if __name__ == '__main__':
      app.run()
