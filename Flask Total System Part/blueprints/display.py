from flask import  Blueprint,render_template,jsonify,redirect,url_for,session
import config
import pymysql
import pandas as pd
import json
import numpy as np
from jinja2 import Markup


bp = Blueprint('display',__name__,url_prefix='/data/display')

col = ['total_price','unit_price','square','size','floor','direction','type','district',
       'nearby','community','decoration','elevator','elevatorNum','ownership']
#从数据库读取二手房数据
df = pd.read_sql_table(table_name='sh_data',con=config.SQLALCHEMY_DATABASE_URI,)
#对数据按需分组
def datalist_bar():
    g = df.groupby('district')
    df_region = g.count()['community']
    x = df_region.index.tolist()
    y = df_region.values.tolist()
    x_y = [list(z) for z in zip(x, y)]
    datalist = {}
    for i in range(8):
        datalist[x[i]] = y[i]
    return datalist
#折柱混合图数据分组
def datalist_bar_line():
    g = df.groupby('district')
    df_region = g.count()['title']
    x1 = df_region.index.tolist()
    y1 = df_region.values.tolist()
    count = 0
    list_return = []
    list = []
    list_1 = []
    list_0 = []
    list_total = y1
    for i in g:
        g_ele = i[1].groupby('elevator')
        df_g_ele = g_ele.count()['title']
        x2 = df_g_ele.index.tolist()
        y2 = df_g_ele.values.tolist()
        for ii in range(2):
            x3 = x2[ii]
            y3 = y2[ii]
            dist = {x3: y3}
            count += 1
            list.append(dist)
            if x3 == '有':
                list_1.append(y3)
            if x3 == '无':
                list_0.append(y3)
    list_return.append(list_1)
    list_return.append(list_0)
    list_return.append(list_total)
    return list_return
#大数据量柱图数据分组
def datalist_bigData():
    list_tp = []
    list_com = []
    list_big = []
    df_tp = df.loc[:, ['total_price']]
    df_com = df.loc[:, ['community']]
    test_tp = np.array(df_tp)
    num = df_tp.count()
    array_tp = df_tp.values.tolist()
    array_com = df_com.values.tolist()
    for i in range(num['total_price']):
        list_tp.append(array_tp[i][0])
        list_com.append(array_com[i][0])
    list_big.append(list_tp)
    list_big.append(list_com)
    return list_big
#3D柱状图数据分组--类名
def datalist_3d():
    list_merge = []
    list_up = []
    list_dis = []
    list_flo = []
    df_thr = df.loc[:, ['floor', 'district', 'unit_price']]
    df_gb = df_thr.groupby('floor')
    x_1 = df_thr.index.tolist()
    y_1 = df_thr.values.tolist()
    count = 0
    for i in df_gb:
        g_thr = i[1].groupby('district')
        y_2 = i[1].values.tolist()  # 数组形式[[1,2,3],[x,y,z]]
        for ii in g_thr:
            # floor
            avg_mean = ii[1].loc[:, ['unit_price']].mean()
            avg_flo = ii[1].loc[:, ['floor']].iloc[[0], [0]]
            flo = avg_flo['floor'].tolist()
            list_flo.append(''.join(flo))
            # unit_price
            avg = int(avg_mean[0])
            list_up.append(avg)
            # district
            avg_dis = ii[1].loc[:, ['district']].iloc[[0], [0]]
            dis = avg_dis['district'].tolist()
            list_dis.append(''.join(dis))
    list_merge.append(list_dis)
    list_merge.append(list_flo)
    list_merge.append(list_up)
    return list_merge
#3D柱状图数据分组--数据
def datalist_3d_data():
    # 3D柱状图分组
    list_merge = []
    list_to = []
    list_up = []
    list_dis = []
    list_flo = []
    df_thr = df.loc[:, ['floor', 'district', 'unit_price']]
    df_gb = df_thr.groupby('floor')
    x_1 = df_thr.index.tolist()
    y_1 = df_thr.values.tolist()
    count = 0
    for i in df_gb:
        g_thr = i[1].groupby('district')
        y_2 = i[1].values.tolist()  # 数组形式[[1,2,3],[x,y,z]]
        for ii in g_thr:
            count += 1
            # floor
            avg_mean = ii[1].loc[:, ['unit_price']].mean()
            avg_flo = ii[1].loc[:, ['floor']].iloc[[0], [0]]
            flo = avg_flo['floor'].tolist()
            list_flo.append(''.join(flo))
            # unit_price
            avg = int(avg_mean[0])
            list_up.append(avg)
            # district
            avg_dis = ii[1].loc[:, ['district']].iloc[[0], [0]]
            dis = avg_dis['district'].tolist()
            list_dis.append(''.join(dis))
    list_merge.append(list_dis)
    list_merge.append(list_flo)
    list_merge.append(list_up)
    num = [[0 for i in range(3)] for j in range(count)]
    for n in range(count):
        num[n][0] = list_dis[n]
        num[n][1] = list_flo[n]
        num[n][2] = list_up[n]
    return num
#纹理饼图——楼型
def datalist_pie_type():
    g_typ = df.groupby('type')
    df_typ = g_typ.count()['title']
    x_typ = df_typ.index.tolist()
    y_typ = df_typ.values.tolist()
    len(x_typ)
    list3=[]
    for n in range(len(x_typ)):
        print(y_typ[n])
        list3.append({"name":x_typ[n], "value":y_typ[n]})
    return list3
#纹理饼图——朝向
def datalist_pie_direction():
    g_dir = df.groupby('direction')
    df_dir = g_dir.count()['title']
    x_dir = df_dir.index.tolist()
    y_dir = df_dir.values.tolist()
    len(x_dir)
    list3 = []
    for n in range(len(x_dir)):
        list3.append({"name": x_dir[n], "value": y_dir[n]})
    return list3
#纹理饼图——户型
def datalist_pie_size():
    g_siz = df.groupby('size')
    df_siz = g_siz.count()['title']
    x_siz = df_siz.index.tolist()
    y_siz = df_siz.values.tolist()
    len(x_siz)
    list3 = []
    for n in range(len(x_siz)):
        list3.append({"name": x_siz[n], "value": y_siz[n]})
    return list3
#纹理饼图——装修
def datalist_pie_decoration():
    g_dec = df.groupby('decoration')
    df_dec = g_dec.count()['title']
    x_dec = df_dec.index.tolist()
    y_dec = df_dec.values.tolist()
    len(x_dec)
    list3 = []
    for n in range(len(x_dec)):
        list3.append({"name": x_dec[n], "value": y_dec[n]})
    return list3
#折线叠加图
def datalist_line():
    list_ld = []  # 地级市列表
    list_ltp_bef = []  # 房价列表整理前
    num_ltp = [[0 for i in range(8)] for j in range(4)]  # 房价列表整理后
    df_line = df.loc[:, ['district', 'decoration', 'total_price']]
    g_line = df_line.groupby('district')
    x_a = df_line.index.tolist()
    y_a = df_line.values.tolist()
    list_ldec = df_line.groupby('decoration').count().index.tolist()#装修情况
    for i in g_line:
        g_dec = i[1].groupby('decoration')
        y_b = i[1].values.tolist()  # 数组形式[[1,2,3],[x,y,z]]
        line_dis = i[1].loc[:, ['district']].iloc[[0], [0]]
        list_ld.append(''.join(line_dis['district'].tolist()))
        for ii in g_dec:
            avg_tp = ii[1].loc[:, ['total_price']].mean()
            avg_dec = ii[1].loc[:, ['decoration']].iloc[[0], [0]]
            list_ltp = str(int(avg_tp['total_price'].tolist()))
            list_ltp_bef.append(''.join(list_ltp))
    for x in range(8):
        num_ltp[0][x] = list_ltp_bef[4 * x]
    for x in range(8):
        num_ltp[1][x] = list_ltp_bef[4 * x + 1]
    for x in range(8):
        num_ltp[2][x] = list_ltp_bef[4 * x + 2]
    for x in range(8):
        num_ltp[3][x] = list_ltp_bef[4 * x + 3]
    print(num_ltp)
    return num_ltp
#散点图
def datalist_scatter():
    df_sc = df.loc[:, ['square', 'total_price']]
    count = df_sc.count()
    num_sc = [[0 for i in range(2)] for j in range(count[0])]
    list_sq = df_sc.loc[:, ['square']].values.tolist()
    list_tpr = df_sc.loc[:, ['total_price']].values.tolist()
    for j in range(count[0]):
        num_sc[j][0] = list_sq[j][0]
        num_sc[j][1] = list_tpr[j][0]*10000
    return num_sc

@bp.route('/bar')
def Bar_chart():
    # 折柱混合图
    list_bar_line = datalist_bar_line()
    print(list_bar_line)
    #大数据量柱图
    list_bigData = datalist_bigData()
    print(list_bigData)
    #3D柱状图
    list_3d = datalist_3d()
    list_3d_data = datalist_3d_data()
    print(list_3d,list_3d_data)
    return render_template('display-bar.html',datalist1=json.dumps(datalist_bar()),bar_line = list_bar_line, bigData = list_bigData, bar_3d =list_3d, bar_3d_data = list_3d_data)

@bp.route('/pie')
def Pie_chart():
    #纹理饼图——楼型
    list_pie_type = datalist_pie_type()
    #纹理饼图——朝向
    list_pie_direction = datalist_pie_direction()
    #纹理饼图——户型
    list_pie_size = datalist_pie_size()
    #纹理饼图——装修
    list_pie_decoration = datalist_pie_decoration()
    return render_template('display-pie.html', datalist5=json.dumps(datalist_bar()), pie_type = list_pie_type, pie_direction = list_pie_direction, pie_size = list_pie_size, pie_decoration = list_pie_decoration)

@bp.route('/line')
def Line_chart():
    #折线叠加图
    list_line = datalist_line()
    return render_template('display-line.html', line = list_line)

@bp.route('/scatter')
def scatter():
    #散点图
    list_scatter = datalist_scatter()
    return render_template('display-scatter.html', scatter = list_scatter)


