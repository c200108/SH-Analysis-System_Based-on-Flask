
import csv
import pymysql



#写入CSV
def write_csv(example_1):
    csvfile = open('二手房数据.csv', mode='a', encoding='utf-8', newline='')
    fieldnames = ['title', 'total_price', 'unit_price', 'square', 'size', 'floor','direction','type',
                  'BuildTime','district','nearby', 'community', 'decoration', 'elevator','elevatorNum','ownership']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writerow(example_1)

#写入数据库
def write_db(example_2):
    conn = pymysql.connect(host='127.0.0.1',port= 3306,user='changziru',
                           password='ru123321',database='secondhouse_wf',charset='utf8mb4'
                           )
    cursor =conn.cursor()
    title = example_2.get('title', '')
    total_price = example_2.get('total_price', '0')
    unit_price = example_2.get('unit_price', '')
    square = example_2.get('square', '')
    size = example_2.get('size', '')
    floor = example_2.get('floor', '')
    direction = example_2.get('direction', '')
    type = example_2.get('type', '')
    BuildTime = example_2.get('BuildTime','')
    district = example_2.get('district', '')
    nearby = example_2.get('nearby', '')
    community = example_2.get('community', '')
    decoration = example_2.get('decoration', '')
    elevator = example_2.get('elevator', '')
    elevatorNum = example_2.get('elevatorNum', '')
    ownership = example_2.get('ownership', '')
    cursor.execute('insert into wf (title, total_price, unit_price, square, size, floor,direction,type,BuildTime,district,nearby, community, decoration, elevator,elevatorNum,ownership)'
                   'values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                   [title, total_price, unit_price, square, size, floor,direction,type,
                  BuildTime,district,nearby, community, decoration, elevator,elevatorNum,ownership])
    conn.commit()#传入数据库
    conn.close()#关闭数据库
