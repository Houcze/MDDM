import click
import json
from config import *


@click.group()
def find():
    pass


@find.command()
@click.option('--id', default=None, help='station id')
def station(id):
    """python find id --id xx"""
    if id:
        for t1 in time.keys():
            for dom in domain:
                for v in variable:
                    data_base = '{}_{}_{}'.format(t1, dom, v) 
                    db = client[data_base]
                    for t2 in time[t1]:
                        this_id = db[t2].find(
                            {"id":{"$eq":int(id)}}
                        )
                        this_collection = []
                        for item in this_id:
                            item.pop('_id')
                            print(item)
                            this_collection.append(item)
                        with open('.\\nuist\\{}_{}_{}_{}_{}.json'.format(t1[:4], dom, v, t2, id), 'w', encoding='utf-8') as file:
                            json.dump(this_collection, file)
                              
@find.command()
@click.option('--llat', default=None, help='lower lat')
@click.option('--llon', default=None, help='lower lon')
@click.option('--ulat', default=None, help='upper lat')
@click.option('--ulon', default=None, help='upper lat')
@click.option('--filetype', default=None, help='file format to save as (In this version json and txt is supported)')
def area(llat, llon, ulat, ulon, filetype):
    """python find.py area --llat xx --llon xx --ulat xx --ulon xx"""
    if llat and llon and ulat and ulon:
        """使用4个输入控制器来锁定范围"""
        for t1 in time.keys():
            print(t1)
            """对数据库的操作"""
            for dom in domain:
                for v in variable:
                    data_base = '{}_{}_{}'.format(t1, dom, v)
                    db = client[data_base]
                    for t2 in time[t1]:
                        """对数据库中表的操作"""
                        this_area = db[t2].find(
                            {'1':{"$gte":float(llon), "$lte":float(ulon)}, "2":{"$gte":float(llat), "$lte":float(ulat)}},
                        )
                
                        this_collection = []
                        for item in this_area:
                            """移除doc id"""
                            item.pop('_id')
                            print(item)
                            """此处获得的item是一个字典"""
                            this_collection.append(item)
                        if filetype == 'json':
                            with open('.\\nuist\\{}_{}_{}_{}.json'.format(t1[:4], dom, v, t2), 'w', encoding='utf-8') as file:
                                json.dump(this_collection, file)
                        elif filetype == 'txt':
                            with open('.\\nuist\\{}_{}_{}_{}.txt'.format(t1[:4], dom, v, t2), 'w', encoding='utf-8') as file:
                                for item in this_collection:
                                    file.write(str(item)[1:-1].replace('\'', ''))
                                    file.write('\n')     
                        else:
                            print('Unsupported format')


if __name__ == '__main__':
    find()