# 1. 导入线性回归模型
from sklearn.linear_model import LinearRegression
# 2. 进行线性回归的预测
def linear_model_main(X_parameter, Y_paramter, predict_value):

    # 2.1 建立线性回归模型
    regr = LinearRegression()

    # 2.2 训练模型
    regr.fit(X_parameter, Y_paramter)

    # 2.3 预测新的样本
    predict_outcome = regr.predict(predict_value)

    # 2.4 返回预测新值
    return predict_outcome


if __name__ == '__main__':
    # 数据源 x广告投入的数量  y销售额 可以预测y的过去和未来
    X = [[4], [8], [9], [8], [7], [12], [6], [10], [6], [9]]
    Y = [9, 20, 22, 15, 17, 23, 18, 25, 10, 20]


    predict_value=4
    predict_outcome = linear_model_main(X, Y, predict_value)
    print('Predicted value:', predict_outcome)