import time
import re
from api.backtrack_use.mongodb_link import origin,events_tracking
"""
该文件提供了事件回溯接口需要使用到的基本接口函数
"""

#国家映射词典，从'CHN'映射到中文名
#还不完全
country_dict={'CHN': '中国', 'USA': '美国', 'HKG': '香港',
              'KOR': '韩国',  'RUS': '俄罗斯', 'ITA': '意大利', 'CZE': '捷克',  'JPN': '日本','FRA': '法国',
              'GHA': '加纳', 'MEX': '墨西哥', 'NZL': '新西兰','EGY': '埃及'}


def timestr2stamp10(time_str):
    #将'20180501'的字符串转换为10位时间戳
    return int(time.mktime(time.strptime(time_str, "%Y%m%d")))

def timestr2stamp13(timestr):
    #将形如"20180506"的时间字符串转换成13位时间戳整数，便于前端展示
    return int(time.mktime(time.strptime(timestr,'%Y%m%d'))*1000)

def senid2index(sentid):
    #将形如"592436239afc10f2c9a240c8_12"的SENTID分解为id和index，其中，index转换为整数
    res=sentid.split('_')
    id=res[0]
    index=int(res[1])
    return id,index

def create_time_dict(start,end):
    #根据提供的开始和结束时间（字符串），生成这期间的所有日期构成的字典
    #便于根据日期统计热度
    #返回的字典形如：{'20180501': 0, '20180502': 0, '20180503': 0}
    start_int = timestr2stamp10(start)
    end_int = timestr2stamp10(end)
    ret_data = {start: 0}
    begin = start_int + 86400
    while begin <= end_int:
        # 生成从START到END的日期，ret_data为返回数据
        time_tmp = time.strftime("%Y%m%d", time.localtime(begin))
        ret_data[time_tmp] = 0
        begin = begin + 86400
    print(ret_data)
    return ret_data

def gkg_person_list(data):
    #提取GKG中的人物名称
    #将gkg中的person字符串转换成list
    list=[]
    if(data==""):
        return list
    list=data.split(';')
    return list

def gkg_country_extract(text):
    #提取GKG中的国家名称
    #返回提取到的三字符信息list
    country_pattern = re.compile("[A-Z]{3}")
    match = re.finditer(country_pattern, text)
    res=[]
    for item in match:
        res.append(item.group(0))
    return res

def dict_sort(dict,num):
    #将dict按值排序，返回前num位的二维数组，每个数字包含key,value
    items=dict.items()
    backitem=[[v[1],v[0]] for v in items]
    backitem.sort(reverse=True)
    backitem=backitem[:10]
    for item in backitem:
        item.reverse()
    return backitem

def data2html(data):
    #将形如{'20180501': 607, '20180502': 0, '20180503': 0, '20180504': 0, '20180505': 0, '20180506': 0}
    #的字典数据转换为前端输入的LIST数据
    ret={'hot':[]}
    max_value=-1
    min_value=0
    for key in data:
        ret['hot'].append([timestr2stamp13(key),data[key]])
        if data[key]>max_value:
            max_value=data[key]
    ret['hot'].sort()
    ret['max_value']=max_value
    ret['min_value']=min_value
    print(ret)
    return ret