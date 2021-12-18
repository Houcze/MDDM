import os
import json
import argparse
import webbrowser
from config import *
from table import table
from tqdm import tqdm


parser = argparse.ArgumentParser(
    description='Process MICAPS Data.'
)

parser.add_argument('--mode', type=str, required=True, help='区域(area) / 站点(id) / 数据格式介绍 (inc)')
parser.add_argument('--id', type=str, help='站点的编号 (Must be set when search arg is set)')
parser.add_argument('--area', type=str, help='经度和纬度的限制 (Must be set when area arg is set)')
parser.add_argument('--year', type=str, help='年')
parser.add_argument('--month', type=str, help='月')
parser.add_argument('--day', type=str, help='日')
parser.add_argument('--hour', type=str, help='当天的时辰')
parser.add_argument('--variable', type=str, help='要检索的变量')
parser.add_argument('--output', type=str, help='将数据下载到这个文件夹')
args = parser.parse_args()
print(args.output)


def get_days(year, month):
    year = int(year)
    month = int(month)
    if year % 4 == 0:
        if month == 2:
            return 29
    if month in (1, 3, 5, 7, 8, 10, 12):
        return 31
    elif month in (4, 6, 9, 11):
        return 30
    elif month == 2:
        return 28
    else:
        print('Valid input.')

def open_readme():
    url = '{}\docs\MICAPS4.pdf'.format(os.getcwd())
    webbrowser.open(url, new=2)
    
########### 预处理，将所有的str展开 ############
if args.year:
    year = [int(y) for y in args.year.split(',')]
if args.month:
    month = [int(m) for m in args.month.split(',')]
if args.day:
    day = [int(d) for d in args.day.split(',')]
if args.hour:
    hour = [int(h) for h in args.hour.split(',')]
if args.variable:
    variable = [v for v in args.variable.split(',')]

if args.id:
    id = [i for i in args.id.split(',')]
    id = [int(i) for i in id]
if args.area:
    area = args.area.split(',')
    if len(area) != 4:
        print('该选项必须提供4个参数！')
    llat, llon, ulat, ulon = area

#############################################

str_date = '{}-{}-{}-{}-00-00' # 时间字符串的基本格式
SURFACE = client['SURFACE'].list_collection_names()
UPPER_AIR = client['UPPER_AIR'].list_collection_names()

v2db = {}
search_list = {}
if args.variable:
    for v in variable:
        search_list[v] = []
        for y in year:
            for m in month:
                y = str(y)
                m = str(m).zfill(2)
                for d in day:
                    for h in hour:
                        search_list[v].append(str_date.format(y, m, str(d).zfill(2), str(h).zfill(2)))
        if v in SURFACE:
            v2db[v] = client['SURFACE']
        elif v in UPPER_AIR:
            v2db[v] = client['UPPER_AIR']
        else:
            print('Invalid Input')

print(search_list)
this_collection = []
if args.mode == 'id':
    if args.id:
        for i in id:
            for v, t_str in search_list.items():
                #this_collection = []
                this_id = v2db[v][v].find(
                    {"id":i}
                )
                for item in this_id:
                    item.pop('_id')
                    if item['date'] in t_str:
                        this_collection.append(item)
                print(this_collection)
                with open(r'{}\{}.txt'.format(args.output, i), 'w', encoding='utf-8') as file:
                    for record in this_collection:
                        for k in record:
                            if k in table.keys():
                                file.write(table[k] + ':' + str(record[k]) + '\n')
                            else:
                                file.write(k + ':' + str(record[k]) + '\n')
            this_collection = []
    else:
        print('当使用id检索模式的时候必须指定id参数')
elif args.mode == 'area':
    if args.area:
        for v, t_str in search_list.items():
            this_area = v2db[v][v].find(
                {'1':{"$gte":float(llon), "$lte":float(ulon)}, "2":{"$gte":float(llat), "$lte":float(ulat)}},
            )
            for item in this_area:
                item.pop('_id')
                if item['date'] in t_str:
                    this_collection.append(item)
            print(this_collection)
            print(args.output)
            with open(r'{}\{}.{}.txt'.format(args.output, args.area, v), 'w', encoding='utf-8') as file:
                for record in this_collection:
                    for k in record:
                        if k in table.keys():
                            file.write(table[k] + ':' + str(record[k]) + '\n')
                        else:
                            file.write(k + ':' + str(record[k]) + '\n')
    else:
        print('')
elif args.mode == 'inc':
    open_readme()
else:
    pass
