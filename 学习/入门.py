# 导入Flask类
from flask import Flask

# 实例化Flask类得到一个对象
# static_folder 这个参数 static
# static_url_path 默认值 /static
app = Flask(__name__)


# app的配置
# 1. 创建一个带有配置信息的类
class Config:
    DEBUG = False


#
# # 2. 完成对app的配置 from_object()
app.config.from_object(Config)


# 定义一个视图函数
@app.route('/index')
def hello():
    return 'hello world'


# 整数 获取地址中的整数 并在函数内容 返回
@app.route('/house/<int:h_id>')
def house_id(h_id):
    return 'the house id is %d' % h_id


# 字符串 获取地址中的字符串 并在函数内 返回
@app.route('/page/<page_str>')
def page_info(page_str):
    return 'the page info is %s' % page_str


@app.route('/')
def index_error():
    print(2 // 0)
    return '2//0 是一个错误的数学公式'


# 启动flask程序
if __name__ == '__main__':
    app.run(  debug=True)  # 使用了 run（）函数后  flask程勋 便会进入到消息循环中  这个时候 它会去监听127.0.0.1:5000下面的请求 循环监听的过程 如果没有获取到请求 也会一直监听 知道程序结束为止
    # app.run() # 127.0.0.0地址下 时候  可以保护我们的代码 外部用户 无法访问  当我们使用了host='0.0.0.0' 之后 外部用户 就可以获取响应信息
    # print('程序开始运行了')  # 在app.run（）后面的所有代码 在flask程序运行期间 是不会被执行的 只有flask结束了 才会被执行
