#爬取链家二手房详情页信息
import time
from random import randint
import requests
from lxml import etree
from secondhouse_spider.Spider_wf import write_csv,write_db

#模拟浏览器操作
USER_AGENTS = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
]
#随机USER_AGENTS
random_agent = USER_AGENTS[randint(0, len(USER_AGENTS) - 1)]
headers = {'User-Agent': random_agent,}

class SpiderFunc:
    def __init__(self):
        self.count = 0
    def spider(self ,list):
        for sh in list:
            response = requests.get(url=sh, params={'param':'1'},headers={'Connection':'close'}).text
            tree = etree.HTML(response)
            li_list = tree.xpath('//ul[@class="sellListContent"]/li[@class="clear LOGVIEWDATA LOGCLICKDATA"]')
            for li in li_list:
                # 获取每套房子详情页的URL
                detail_url = li.xpath('.//div[@class="title"]/a/@href')[0]
                try:
                    # 向每个详情页发送请求
                    detail_response = requests.get(url=detail_url, headers={'Connection': 'close'}).text

                except Exception as e:
                    sleeptime = randint(15,30)
                    time.sleep(sleeptime)#随机时间延迟
                    print(repr(e))#打印异常信息
                    continue
                else:
                    detail_tree = etree.HTML(detail_response)
                    item = {}
                    title_list = detail_tree.xpath('//div[@class="title"]/h1/text()')
                    item['title'] = title_list[0] if title_list else None  # 1简介

                    total_price_list = detail_tree.xpath('//span[@class="total"]/text()')
                    item['total_price'] = total_price_list[0] if total_price_list else None  # 2总价

                    unit_price_list = detail_tree.xpath('//span[@class="unitPriceValue"]/text()')
                    item['unit_price'] = unit_price_list[0] if unit_price_list else None  # 3单价

                    square_list = detail_tree.xpath('//div[@class="area"]/div[@class="mainInfo"]/text()')
                    item['square'] = square_list[0] if square_list else None  # 4面积

                    size_list = detail_tree.xpath('//div[@class="base"]/div[@class="content"]/ul/li[1]/text()')
                    item['size'] = size_list[0] if size_list else None  # 5户型

                    floor_list = detail_tree.xpath('//div[@class="base"]/div[@class="content"]/ul/li[2]/text()')
                    item['floor'] = floor_list[0] if floor_list else None#6楼层

                    direction_list = detail_tree.xpath('//div[@class="type"]/div[@class="mainInfo"]/text()')
                    item['direction'] = direction_list[0] if direction_list else None  # 7朝向

                    type_list = detail_tree.xpath('//div[@class="area"]/div[@class="subInfo"]/text()')
                    item['type'] = type_list[0] if type_list else None  # 8楼型

                    BuildTime_list = detail_tree.xpath('//div[@class="transaction"]/div[@class="content"]/ul/li[5]/span[2]/text()')
                    item['BuildTime'] = BuildTime_list[0] if BuildTime_list else None  # 9房屋年限

                    district_list = detail_tree.xpath('//div[@class="areaName"]/span[@class="info"]/a[1]/text()')
                    item['district'] = district_list[0] if district_list else None  # 10地区

                    nearby_list = detail_tree.xpath('//div[@class="areaName"]/span[@class="info"]/a[2]/text()')
                    item['nearby'] = nearby_list[0] if nearby_list else None  # 11区域

                    community_list = detail_tree.xpath('//div[@class="communityName"]/a[1]/text()')
                    item['community'] = community_list[0] if community_list else None  # 12小区

                    decoration_list = detail_tree.xpath('//div[@class="base"]/div[@class="content"]/ul/li[9]/text()')
                    item['decoration'] = decoration_list[0] if decoration_list else None  # 13装修

                    elevator_list = detail_tree.xpath('//div[@class="base"]/div[@class="content"]/ul/li[11]/text()')
                    item['elevator'] = elevator_list[0] if elevator_list else None  # 14电梯

                    elevatorNum_list = detail_tree.xpath('//div[@class="base"]/div[@class="content"]/ul/li[10]/text()')
                    item['elevatorNum'] = elevatorNum_list[0] if elevatorNum_list else None  # 15梯户比例

                    ownership_list = detail_tree.xpath('//div[@class="transaction"]/div[@class="content"]/ul/li[2]/span[2]/text()')
                    item['ownership'] = ownership_list[0] if ownership_list else None  # 16交易权属
                    self.count += 1
                    print(self.count,title_list)

                    # 将爬取到的数据存入CSV文件
                    write_csv(item)
                    # 将爬取到的数据存取到MySQL数据库中
                    write_db(item)
#循环目标网站
count =0
for page in range(1,101):
    if page <=40:
        url_qingzhoushi = 'https://wf.lianjia.com/ershoufang/qingzhoushi/pg' + str(page)  # 青州市40
        url_hantingqu = 'https://wf.lianjia.com/ershoufang/hantingqu/pg' + str(page)  # 寒亭区 76
        url_fangzi = 'https://wf.lianjia.com/ershoufang/fangziqu/pg' + str(page)  # 坊子区
        url_kuiwenqu = 'https://wf.lianjia.com/ershoufang/kuiwenqu/pg' + str(page)  # 奎文区
        url_gaoxin = 'https://wf.lianjia.com/ershoufang/gaoxinjishuchanyekaifaqu/pg' + str(page)  # 高新区
        url_jingji = 'https://wf.lianjia.com/ershoufang/jingjijishukaifaqu2/pg' + str(page)  # 经济技术85
        url_shouguangshi = 'https://wf.lianjia.com/ershoufang/shouguangshi/pg' + str(page)  # 寿光市 95
        url_weichengqu = 'https://wf.lianjia.com/ershoufang/weichengqu/pg' + str(page)  # 潍城区
        list_wf = [url_qingzhoushi, url_hantingqu,url_jingji, url_shouguangshi, url_weichengqu, url_fangzi, url_kuiwenqu, url_gaoxin]
        SpiderFunc().spider(list_wf)
    elif page <=76:
        url_hantingqu = 'https://wf.lianjia.com/ershoufang/hantingqu/pg' + str(page)  # 寒亭区 76
        url_fangzi = 'https://wf.lianjia.com/ershoufang/fangziqu/pg' + str(page)  # 坊子区
        url_kuiwenqu = 'https://wf.lianjia.com/ershoufang/kuiwenqu/pg' + str(page)  # 奎文区
        url_gaoxin = 'https://wf.lianjia.com/ershoufang/gaoxinjishuchanyekaifaqu/pg' + str(page)  # 高新区
        url_jingji = 'https://wf.lianjia.com/ershoufang/jingjijishukaifaqu2/pg' + str(page)  # 经济技术85
        url_shouguangshi = 'https://wf.lianjia.com/ershoufang/shouguangshi/pg' + str(page)  # 寿光市 95
        url_weichengqu = 'https://wf.lianjia.com/ershoufang/weichengqu/pg' + str(page)  # 潍城区
        list_wf = [url_hantingqu,url_jingji, url_shouguangshi, url_weichengqu, url_fangzi, url_kuiwenqu, url_gaoxin]
        SpiderFunc().spider(list_wf)
    elif page<=85:
        url_fangzi = 'https://wf.lianjia.com/ershoufang/fangziqu/pg' + str(page)  # 坊子区
        url_kuiwenqu = 'https://wf.lianjia.com/ershoufang/kuiwenqu/pg' + str(page)  # 奎文区
        url_gaoxin = 'https://wf.lianjia.com/ershoufang/gaoxinjishuchanyekaifaqu/pg' + str(page)  # 高新区
        url_jingji = 'https://wf.lianjia.com/ershoufang/jingjijishukaifaqu2/pg' + str(page)  # 经济技术85
        url_shouguangshi = 'https://wf.lianjia.com/ershoufang/shouguangshi/pg' + str(page)  # 寿光市 95
        url_weichengqu = 'https://wf.lianjia.com/ershoufang/weichengqu/pg' + str(page)  # 潍城区
        list_wf = [url_jingji, url_shouguangshi, url_weichengqu, url_fangzi, url_kuiwenqu, url_gaoxin]
        SpiderFunc().spider(list_wf)
    elif page <=95:
        url_shouguangshi = 'https://wf.lianjia.com/ershoufang/shouguangshi/pg' + str(page)  # 寿光市 95
        url_weichengqu = 'https://wf.lianjia.com/ershoufang/weichengqu/pg' + str(page)  # 潍城区
        url_fangzi = 'https://wf.lianjia.com/ershoufang/fangziqu/pg' + str(page)  # 坊子区
        url_kuiwenqu = 'https://wf.lianjia.com/ershoufang/kuiwenqu/pg' + str(page)  # 奎文区
        url_gaoxin = 'https://wf.lianjia.com/ershoufang/gaoxinjishuchanyekaifaqu/pg' + str(page)  # 高新区
        list_wf = [url_shouguangshi, url_weichengqu, url_fangzi, url_kuiwenqu, url_gaoxin]
        SpiderFunc().spider(list_wf)
    else:
        url_weichengqu = 'https://wf.lianjia.com/ershoufang/weichengqu/pg' + str(page)  # 潍城区
        url_fangzi = 'https://wf.lianjia.com/ershoufang/fangziqu/pg' + str(page)  # 坊子区
        url_kuiwenqu = 'https://wf.lianjia.com/ershoufang/kuiwenqu/pg' + str(page)  # 奎文区
        url_gaoxin = 'https://wf.lianjia.com/ershoufang/gaoxinjishuchanyekaifaqu/pg' + str(page)  # 高新区
        list_wf = [url_weichengqu, url_fangzi,url_kuiwenqu, url_gaoxin]
        SpiderFunc().spider(list_wf)







