from wordcloud import WordCloud
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
mask = np.array(Image.open("词云背景图.png"))


f = open('词云.txt','r',encoding = 'utf-8')
txt = f.read()
f.close
wordcloud = WordCloud(
    stopwords= {'暂无数据','有','无'},
    scale= 8,
    font_path="simkai.ttf",
    background_color= 'white',
    width = 800,
    height = 600,
    max_words = 300,
    max_font_size = 80,
    mask = mask,
    contour_width = 3,
    contour_color = 'steelblue'
).generate(txt)
wordcloud.to_file('词云图.png')

