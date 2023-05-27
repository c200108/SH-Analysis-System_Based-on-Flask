# SH-Analysis-System_Based-on-Flask

Web Programme(Web程序) == WeiFang Second-hand House Data Analysis And Forecast System（潍坊市二手房数据分析预测系统）

这个项目是我的本科毕业设计《基于Python的二手房数据分析预测系统》，**遵循MVT设计模式，基于B/S架构与高内聚低耦合原则，整个项目开发按照四个步骤进行：需求分析、数据获取、系统搭建与测试部署**。

<img src="https://github.com/c200108/SH-Analysis-System_Based-on-Flask/blob/main/1.png?raw=true" style="zoom: 80%;" />

如果有类似课题的同学，可以参考一下。

项目结构解读

- Flask Total System Part——基于Flask的整体网站系统
  - blueprints——蓝图(V)
    - display.py：可视化图表模块
    - forecast.py：预测模块
    - forms.py：表单验证模块
    - func.py：一级页面模块
    - user.py：用户模块
  - static——静态资源(V)
  - templates——模板文档(T)
  - app.py：启动文件
  - config.py：配置信息
  - exts.py：插件
  - models.py：模型文件(M)
- Second-hand House Data File——二手房数据文件
  - sh_data.csv：清洗后数据
  - forecast.csv：预测部分所需数据
- Secondhouse_Spider Part——爬虫程序
  - lianjia_house.py：爬虫
  - Spider_wf.py：数据存储程序
- Word Cloud part——词云程序
  - word_cloud.py：生成词云



爬虫程序图：

<img src="https://github.com/c200108/SH-Analysis-System_Based-on-Flask/blob/main/2.png?raw=true" style="zoom:67%;" />



Flask系统结构图：

<img src="https://github.com/c200108/SH-Analysis-System_Based-on-Flask/blob/main/3.png?raw=true" style="zoom: 67%;" />



部署流程图：

<img src="https://github.com/c200108/SH-Analysis-System_Based-on-Flask/blob/main/4.png?raw=true" style="zoom:80%;" />



