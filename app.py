from flask import Flask
from settings import Config, db
from list_page import list_page
from index_page import index_page
from detail_page import detail_page
from use import user_page

app = Flask(__name__)

app.config.from_object(Config)

db.init_app(app)

# 将蓝图注册到app中
app.register_blueprint(index_page, url_prefix='/')
app.register_blueprint(list_page, url_prefix='/')
app.register_blueprint(detail_page, url_prefix='/')
app.register_blueprint(user_page, url_prefix='/')

if __name__ == '__main__':
    app.run(debug=True)
