from flask import  Blueprint,render_template,jsonify,redirect,url_for,session
from exts import mail,db
from flask import request
from models import Quotes
from sqlalchemy.sql import text
import config
import pymysql
import pandas as pd
from pyecharts.charts import *
from pyecharts import options as opts


bp = Blueprint('func',__name__,url_prefix='/')

#http://127.0.0.1:5000
@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/data/query',defaults={'page': 1}, methods=['GET', 'POST'])
@bp.route('/data/query/page/<int:page>')
def data_query(page):
    #搜索框内容模糊匹配
    content_title = request.form.get('title') #从html获取到title输入框中的内容
    content_district = request.form.get('district') #从html获取到district输入框中的内容
    content_community = request.form.get('community')  # 从html获取到community输入框中的内容
    if content_title is None:
        content_title = ""
    # 计算分页数据
    data = Quotes.query.filter(
        Quotes.title.like("%" + content_title + "%") if content_title is not None else text(''),
        Quotes.total_price.like("%" + content_district + "%") if content_district is not None else text(''),
        Quotes.unit_price.like("%" + content_community + "%") if content_community is not None else text(''),
    ).all()
    total_count = len(data)
    page_size = 50
    total_pages = (total_count + page_size - 1) // page_size
    offset = (page - 1) * page_size
    limit = page_size
    return render_template('data-query.html', data=data, offset=offset, limit=limit, page=page, total_pages=total_pages)

@bp.route('/data/display')
def data_display():
    #生成柱状图、饼图、折线图、散点图、地图
    return render_template('data-display.html')

@bp.route('/data/forecast')
def data_forecast():
    return render_template('data-forecast.html')
