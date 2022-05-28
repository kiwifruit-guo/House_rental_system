# 1. 从pymysql中导入connect函数
#2、使用connect函数获取connection对象
# 3. 使用connection对象 获取游标cursor
# 4. 使用游标来执行sql语句
# 5. 使用游标获取 我们想要的结果
# 6. 关闭游标
# 7. 断开与数据库的连接
from pymysql import connect

USERNAME = 'root'
PASSWORD = '123456'
HOST = 'localhost'
PORT = 3306
DATABASE = 'beijing_house_data'

#对数据库下命令
def query_data(sql_str):
    try:
        # 2. 使用connect函数 获取connection对象
        conn = connect(user=USERNAME, password=PASSWORD, host=HOST, port=PORT, database=DATABASE)

        # 3. 使用connection对象 获取游标cursor
        cur = conn.cursor()

        # 4. 使用游标来执行sql语句

        # sql = 'select count(*) from soufang'

        row_count = cur.execute(sql_str)  # execute()函数的执行结果 是返回一个受影响的行数 在本项目中 我们使用不到

        # commit()方法 用来提交修改数据的sql到数据库 如果我们不调用commit（）函数的话 sql是不会在数据库中执行的 与sqlalchemy中的用法相同
        conn.commit()

        # 5. 使用游标获取 我们想要的结果
        result = cur.fetchall()

    except Exception as e:
        print(e)

    finally:
        # 6. 关闭游标
        cur.close()

        # 7. 断开与数据库的连接
        conn.close()

        return result


if __name__ == '__main__':



    #sql_list=['use beijing_house_data','show columns from house_info','alter table house_info drop column liangdian;','show columns from house_info']

    sql_list=['use beijing_house_data','show tables']

    for sql in sql_list:
        result = query_data(sql)
    for i in result:
        print(i[0])

