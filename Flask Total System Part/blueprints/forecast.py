from flask import  Blueprint,render_template,jsonify,redirect,url_for,session,request
import config
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pylab import mpl
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import r2_score
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error

from sqlalchemy import create_engine

bp = Blueprint('forecast',__name__,url_prefix='/data/forecast')

# 从数据库读取二手房数据
df = pd.read_sql_table(table_name='forecast', con=config.SQLALCHEMY_DATABASE_URI)

#一元线性回归模型（房价关于面积的变化关系） guess_square为查询面积
def Simple_linear_regression(guess_square):
    # 转化数据类型
    df['total_price'] = df['total_price'].astype(float)
    df['square'] = df['square'].astype(float)
    # 二手房价格与面积关系可视化
    plt.scatter(df['square'], df['total_price'])
    plt.xlabel('Area')
    plt.ylabel('Total_Price')
    # plt.show()
    # 线性回归模型预测
    model = LinearRegression()
    model.fit(df[['square']], df['total_price'])
    # 预测结果可视化
    plt.scatter(df['square'], df['total_price'])
    plt.plot(df['square'], model.predict(df[['square']]), color='red')
    plt.xlabel('Area')
    plt.ylabel('Total_Price')
    # plt.show() #图表显示
    # 预测一套房源价格
    guess_price = model.predict([[guess_square]])
    avg_unit_price = df['unit_price'].median() / 10000  # 计算单价中位数
    avg_total_price = avg_unit_price * 38  # 计算初始面积38时房屋总价（该一元线性回归模型当面积<=38时房价为非正数，不符合逻辑）
    predicted_price = guess_price[0] + avg_total_price  # 预测值=估计值+偏差值
    result = f'预测：房屋面积为 {guess_square} 平方米时，房屋总价约为 {predicted_price:.2f} 万元'
    return result

#多元线性回归模型（因变量房价关于面积、房间数量、装修情况、楼型、地区、有无电梯、房屋性质等自变量的变化关系）
def Multiple_linear_regression(square_guess,dataSize_new_guess,decoration_guess,type_guess,district_guess,elevator_guess,ownership_guess):
    # 设置显示中文字体
    mpl.rcParams["font.sans-serif"] = ["SimHei"]
    # 设置正常显示符号
    mpl.rcParams["axes.unicode_minus"] = False
    # 选择模型需要的自变量与因变量
    data = df.loc[:,['total_price', 'square', 'dataSize_new', 'decoration', 'type', 'district', 'elevator', 'ownership']]
    # 数据预处理，LabelEncoder是scikit-learn库中的一个编码器，用于将离散型变量转换为数值型变量,将标签编码为连续的数字
    encoder1 = LabelEncoder()
    data['decoration'] = encoder1.fit_transform(data['decoration'])
    encoder2 = LabelEncoder()
    data['type'] = encoder2.fit_transform(data['type'])
    encoder3 = LabelEncoder()
    data['district'] = encoder3.fit_transform(data['district'])
    encoder4 = LabelEncoder()
    data['elevator'] = encoder4.fit_transform(data['elevator'])
    encoder5 = LabelEncoder()
    data['ownership'] = encoder5.fit_transform(data['ownership'])
    # 划分训练集和测试集
    X = data.drop(['total_price'], axis=1)
    y = data['total_price']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.16, random_state=42)  # 测试集占总数据集的16%，该条件下R2决定系数最高为0.7228
    # 建立线性回归模型
    model = LinearRegression()
    model.fit(X_train, y_train)
    # 预测房价
    y_pred = model.predict(X_test)
    # 计算模型的评估指标
    r2 = r2_score(y_test, y_pred)
    print('R2 score:', r2)
    # 可视化模型预测效果
    fig, ax = plt.subplots()
    ax.scatter(y_test, y_pred, edgecolors=(0, 0, 0))
    ax.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'k--', lw=4)  # 在散点图上绘制一条对角线，用来表示模型预测值与真实值之间的差距。
    ax.set_xlabel('实际房价')
    ax.set_ylabel('预测房价')
    # plt.show() #图表显示
    # 查看LabelEncoder重编码之后，原来的离散型变量与处理得到的数值型变量之间的对应关系
    print(encoder1.classes_, encoder1.transform(encoder1.classes_))
    print(encoder2.classes_, encoder2.transform(encoder2.classes_))
    print(encoder3.classes_, encoder3.transform(encoder3.classes_))
    print(encoder4.classes_, encoder4.transform(encoder4.classes_))
    print(encoder5.classes_, encoder5.transform(encoder5.classes_))

    # 将输入的字符编码连续的数值型变量，方便后续预测
    def decoration_transform(x):
        if x == '其他':
            return 0
        elif x == '毛坯':
            return 1
        elif x == '简装':
            return 2
        elif x == '精装':
            return 3

    def type_transform(x):
        if x == '塔楼':
            return 0
        elif x == '平房':
            return 1
        elif x == '板塔结合':
            return 2
        elif x == '板楼':
            return 3

    def district_transform(x):
        if x == '坊子区':
            return 0
        elif x == '奎文区':
            return 1
        elif x == '寒亭区':
            return 2
        elif x == '寿光市':
            return 3
        elif x == '潍城区':
            return 4
        elif x == '经济技术开发区':
            return 5
        elif x == '青州市':
            return 6
        elif x == '高新技术产业开发区':
            return 7

    def elevator_transform(x):
        if x == '无':
            return 0
        elif x == '有':
            return 1

    def ownership_transform(x):
        if x == '商品房':
            return 0
        elif x == '房改房':
            return 1

    # 创建待测数据集df_guess，类型为DataFrame,其中值为X_guess,列名为col_name
    X_guess = [[square_guess, dataSize_new_guess, decoration_transform(decoration_guess), type_transform(type_guess),
                district_transform(district_guess), elevator_transform(elevator_guess),
                ownership_transform(ownership_guess)]]
    col_name = ['square', 'dataSize_new', 'decoration', 'type', 'district', 'elevator', 'ownership']
    df_guess = pd.DataFrame(X_guess, columns=col_name)
    # 根据输入的数据集与建立的多元线性回归模型预测房价
    avg_unit_price = df['unit_price'].median() / 10000  # 计算单价中位数
    avg_total_price = avg_unit_price * 48  # 计算初始面积38时房屋总价（该一元线性回归模型当面积<=48时房价为非正数，不符合逻辑）
    result_guess = model.predict(df_guess)
    if (df_guess.square.all()) & (df_guess.dataSize_new.all()):
        result = result_guess + avg_total_price
        result = f'预测：房屋面积为 {square_guess}平方米、房间数量为{dataSize_new_guess}时、装修情况为{decoration_guess}、楼房类型为{type_guess}、县市区为{district_guess}、' \
                 f'{elevator_guess}电梯、房屋性质{ownership_guess}等条件下，房屋总价约为 {result[0]:.2f} 万元'
        return result
    else:
        result = '无法预测'
        return result

#K近邻分类预测模型（因变量房价关于面积、房间数量、装修情况、楼型、地区、有无电梯、房屋性质、楼层、梯户比例等自变量的变化关系）
def KNN(square_guess,dataSize_new_guess,decoration_guess,type_guess,district_guess,elevator_guess,ownership_guess,floor_guess,elevatorNum_guess):
    # 设置显示中文字体
    mpl.rcParams["font.sans-serif"] = ["SimHei"]
    # 设置正常显示符号
    mpl.rcParams["axes.unicode_minus"] = False
    # 选择模型需要的自变量与因变量
    data = df.loc[:,['total_price', 'square', 'dataSize_new', 'decoration', 'type', 'district', 'elevator', 'ownership', 'floor','elevatorNum']]
    # 数据预处理，LabelEncoder用于将离散型变量转换为数值型变量,将标签编码为连续的数字
    encoder1 = LabelEncoder()
    data['decoration'] = encoder1.fit_transform(data['decoration'])
    encoder2 = LabelEncoder()
    data['type'] = encoder2.fit_transform(data['type'])
    encoder3 = LabelEncoder()
    data['district'] = encoder3.fit_transform(data['district'])
    encoder4 = LabelEncoder()
    data['elevator'] = encoder4.fit_transform(data['elevator'])
    encoder5 = LabelEncoder()
    data['ownership'] = encoder5.fit_transform(data['ownership'])
    encoder6 = LabelEncoder()
    data['floor'] = encoder6.fit_transform(data['floor'])
    encoder7 = LabelEncoder()
    data['elevatorNum'] = encoder7.fit_transform(data['elevatorNum'])
    # 拆分特征变量和目标变量
    X = data.drop('total_price', axis=1)
    y = data['total_price']
    # 划分训练集与数据集
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)  # 测试集占总量的20%的情况下，准确率最高
    # 定义要调参的K值列表
    param_grid = {'n_neighbors': range(1, 20)}
    # 创建GridSearchCV对象
    grid_search = GridSearchCV(KNeighborsRegressor(), param_grid, cv=5, scoring='neg_mean_absolute_error')
    # 拟合训练数据
    grid_search.fit(X_train, y_train)
    # 输出最佳参数和对应的交叉验证得分
    print("Best parameter: ", grid_search.best_params_)
    print("Best cross-validation score: {:.2f}".format(-grid_search.best_score_))
    # 创建K近邻算法模型 n_neighbors表示用于预测的最近邻居数量
    knn = KNeighborsRegressor(grid_search.best_params_['n_neighbors'])  # 当K值为grid_search.best_params_时，模型准确率最高
    # 训练模型
    knn.fit(X_train, y_train)
    # 进行预测
    y_pred = knn.predict(X_test)
    # 绘制实际值和预测值的散点图
    fig, ax = plt.subplots()
    plt.scatter(y_test, y_pred)
    ax.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'k--', lw=3)  # 在散点图上绘制一条对角线，用来表示模型预测值与真实值之间的差距。
    plt.xlabel('房价实际值')
    plt.ylabel('房价预测值')
    plt.show()
    # 评估模型
    rmse = mean_squared_error(y_test, y_pred, squared=False)
    print("均方根误差（RMSE）为:", rmse)
    # 计算平均绝对误差
    mae = mean_absolute_error(y_test, y_pred)
    print('平均绝对误差（MAE）为：', mae)
    #计算决定系数
    r2 = r2_score(y_test, y_pred)
    print('R2 score:', r2)

    # 将两个列表合并转换为字典形式
    dist_dec = {}
    dist_typ = {}
    dist_dis = {}
    dist_ele = {}
    dist_own = {}
    dist_flo = {}
    dist_Num = {}
    for i in range(4):
        dist_dec[encoder1.classes_[i]] = encoder1.transform(encoder1.classes_)[i]
    for i in range(4):
        dist_typ[encoder2.classes_[i]] = encoder2.transform(encoder2.classes_)[i]
    for i in range(8):
        dist_dis[encoder3.classes_[i]] = encoder3.transform(encoder3.classes_)[i]
    for i in range(2):
        dist_ele[encoder4.classes_[i]] = encoder4.transform(encoder4.classes_)[i]
    for i in range(2):
        dist_own[encoder5.classes_[i]] = encoder5.transform(encoder5.classes_)[i]
    for i in range(96):
        dist_flo[encoder6.classes_[i].replace(" ","")] = encoder6.transform(encoder6.classes_)[i]
    for i in range(116):
        dist_Num[encoder7.classes_[i]] = encoder7.transform(encoder7.classes_)[i]
    # 创建待测数据集，类型为DataFrame
    X_guess = [[square_guess, dataSize_new_guess, dist_dec[decoration_guess], dist_typ[type_guess], dist_dis[district_guess],
                dist_ele[elevator_guess],dist_own[ownership_guess], dist_flo[floor_guess], dist_Num[elevatorNum_guess]]]
    col_name = ['square', 'dataSize_new', 'decoration', 'type', 'district', 'elevator', 'ownership', 'floor',
                'elevatorNum']
    df_guess = pd.DataFrame(X_guess, columns=col_name)
    # 输入待测数据集并预测
    result = knn.predict(df_guess)
    result = f'预测：房屋面积为 {square_guess}平方米、房间数量为{dataSize_new_guess}时、装修情况为{decoration_guess}、楼房类型为{type_guess}、县市区为{district_guess}、{elevator_guess}电梯、房屋性质{ownership_guess}、楼层为{floor_guess}、梯户比例为{elevatorNum_guess}等条件下，房屋总价约为 {result[0]:.2f} 万元'
    print(result)
    return result

@bp.route('/linear',methods=['GET','POST'])
def linear():
    guess_result_simple = None
    guess_result_multiple = None
    print(request.form)
    if request.method == 'GET':
        return render_template("linear-regression.html")
    else:
        if request.form['btn'] == '立即提交':
            if request.form.get('guesstext') == '':
                guess_result_simple = None
            else:
                content_guess = request.form.get('guesstext')
                content_guess = int(content_guess)
                guess_result_simple = Simple_linear_regression(content_guess)

        elif request.form['btn'] == '确认':
            square_guess = request.form.get('square_guess')
            dataSize_new_guess = request.form.get('dataSize_new_guess')
            decoration_guess = request.form.get('decoration_guess')
            type_guess = request.form.get('type_guess')
            district_guess = request.form.get('district_guess')
            elevator_guess = request.form.get('elevator_guess')
            ownership_guess = request.form.get('ownership_guess')
            guess_result_multiple = Multiple_linear_regression(square_guess,dataSize_new_guess,decoration_guess,type_guess,district_guess,elevator_guess,ownership_guess)
    return render_template('linear-regression.html', simple=guess_result_simple, multiple=guess_result_multiple)

@bp.route('/knn',methods=['GET','POST'])
def knn():
    guess_result_knn = None
    print(request.form)
    if request.method == 'GET':
        return render_template("knn.html")
    else:
        if request.form['btn'] == '确认':
            square_guess = request.form.get('square_guess')
            dataSize_new_guess = request.form.get('dataSize_new_guess')
            decoration_guess = request.form.get('decoration_guess')
            type_guess = request.form.get('type_guess')
            district_guess = request.form.get('district_guess')
            elevator_guess = request.form.get('elevator_guess')
            ownership_guess = request.form.get('ownership_guess')
            floor_guess = request.form.get('floor_guess')
            elevatorNum_guess = request.form.get('elevatorNum_guess')
            guess_result_knn = KNN(square_guess,dataSize_new_guess,decoration_guess,type_guess,district_guess,elevator_guess,ownership_guess,floor_guess,elevatorNum_guess)

    return render_template('knn.html', knn = guess_result_knn)


