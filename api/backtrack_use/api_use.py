import time
import re
from api.backtrack_use.mongodb_link import origin,events_tracking
from api.backtrack_use.event_basic_use import *
"""
事件回溯9个方案所需要的接口函数
每个函数输入相关信息，进行查询统计，返回前端可展示的数据
所用到的基本函数可见api.backtrack_use.event_basic_use
"""

def no1_news_only_search(actor1,actor2,start,end,num=0):
    #方案一，直接查询英文新闻，返回热度图
    #actor1,actor2为长度相等的数组，相同索引位置表示一组
    #num代表检索条数，默认为0，若为0就是全部检索，否则只检索前num条,由于全部搜索可能时间很长，可以只搜一部分

    #先根据日期生成字典，便于统计
    ret_data=create_time_dict(start,end)

    dict={"o_gt":{"$gte":timestr2stamp10(start),"$lte":timestr2stamp10(end)}}
    print(dict)
    cnt=0
    total=len(actor1)
    if num==0:
        res = origin.find(dict)
    else:
        res=origin.find(dict).limit(num)
    #10000条就很慢了
    while True:
        try:
            item=res.next()
            try:
                if 's_cont' in item and 'o_gt' in item:
                    # 查看原文，统计出现次数
                    cnt=0
                    while cnt<total:
                        res1 = re.search(actor1[cnt], item['s_cont'])
                        res2 = re.search(actor2[cnt], item['s_cont'])
                        if res1 is not None and res2 is not None:
                            time_tmp=time.strftime("%Y%m%d",time.localtime(item['o_gt']))
                            if time_tmp in ret_data:
                                ret_data[time_tmp]+=1
                            break
                        cnt+=1
            except:
                continue
        except StopIteration:
            print('finished')
            break
        except Exception as e:
            print(e)
    ret_data=data2html(ret_data)
    print(ret_data)
    return ret_data

def no2_news_only_search(actor1,actor2,start,end):
    #方案二，先查询英文新闻，再联立事件数据库，返回热度图
    #输入输出与no1相同,返回的数据需要经过data2html转化为前端接受的格式

    start_int=timestr2stamp10(start)
    end_int=timestr2stamp10(end)
    ret_data = {start: 0}
    begin = start_int + 86400
    while begin<=end_int:
        #生成从START到END的日期，ret_data为返回数据
        time_tmp=time.strftime("%Y%m%d",time.localtime(begin))
        ret_data[time_tmp]=0
        begin=begin+86400
    print(ret_data)
    dict={"o_gt":{"$gte":timestr2stamp10(start),"$lte":timestr2stamp10(end)}}
    print(dict)
    cnt=0
    total=len(actor1)
    res=origin.find(dict).limit(1000)
    while True:
        try:
            item=res.next()
            try:
                if 's_cont' in item and 'o_gt' in item:
                    # 查看原文
                    cnt=0
                    while cnt<total:
                        res1 = re.search(actor1[cnt], item['s_cont'])
                        res2 = re.search(actor2[cnt], item['s_cont'])
                        if res1 is not None and res2 is not None:
                            #统计事件数据库中的事件个数
                            event_cnt = 0
                            while str(event_cnt) in item['events']:
                                event_cnt += 1
                            if event_cnt!=0:
                                time_tmp=time.strftime("%Y%m%d",time.localtime(item['o_gt']))
                                if time_tmp in ret_data:
                                    ret_data[time_tmp]+=event_cnt
                            break
                        cnt+=1
            except:
                continue
        except StopIteration:
            print('finished')
            break
        except Exception as e:
            print(e)
    ret_data = data2html(ret_data)
    print(ret_data)
    return ret_data


def no3_news_only_search(actor1,actor2,start,end):
    #方案三，先查询英文新闻，再联立GKG数据库，返回人物图
    #输入与no1相同,返回前10位人物及出现次数
    ret_data = {}

    dict={"o_gt":{"$gte":timestr2stamp10(start),"$lte":timestr2stamp10(end)}}

    print(dict)
    cnt=0
    total=len(actor1)
    res=origin.find(dict).limit(1000)
    while True:
        try:
            item=res.next()
            try:
                if 's_cont' in item and 'o_gt' in item:
                    # 查看原文，统计出现次数
                    cnt=0
                    while cnt<total:
                        res1 = re.search(actor1[cnt], item['s_cont'])
                        res2 = re.search(actor2[cnt], item['s_cont'])
                        if res1 is not None and res2 is not None:
                            #统计GKG数据库中的persons个数
                            if item['gkg']['persons']!="":
                                list=gkg_person_list(item['gkg']['persons'])
                                for name in list:
                                    if name not in ret_data:
                                        ret_data[name]=1
                                    else:
                                        ret_data[name]+=1
                            break
                        cnt+=1
            except:
                continue
        except StopIteration:
            print('finished')
            break
        except Exception as e:
            print(e)
    ret_data=dict_sort(ret_data,10)
    name = []
    value = []
    for item in ret_data:
        name.append(item[0])
        value.append(item[1])
    ret_data={}
    ret_data['hot']=value
    ret_data['person']=name
    print(ret_data)
    return ret_data

def no4_news_only_search(actor1,actor2,event,start,end):
    #方案四，先查询事件数据库，返回不同事件类型的热度图
    #输入多了一个事件，返回的数据已经转化为前端接受的格式了
    # actor1 = ["China", "China", "Japan", "", "USA"]
    # actor2 = ["USA", "Trump", "USA", "China", ""]
    # event = [1, 2, 3]
    ret_data = {}
    for event_code in event:
        #循环搜索quadclass
        ret_data[event_code]={}
        cnt=0
        total_length=len(actor1)
        while cnt<total_length:
            #对于每一对actor做一次查询，统计出现的次数
            dict={'actor1name':actor1[cnt],'actor2name':actor2[cnt],'quadclass':event_code,'sqldate':{'$gte':start,'$lte':end}}
            print(dict)
            res=events_tracking.find(dict)
            for item in res:
                if 'sqldate' in item:
                    if item['sqldate'] in ret_data[event_code]:
                        ret_data[event_code][item['sqldate']]+=1
                    else:
                        ret_data[event_code][item['sqldate']]=1
            cnt+=1
    #按照quadclass依此进行类型转换，以适应前端输入格式
    code_map={1:'口头合作',2:'实际合作',3:'口头冲突',4:'实际冲突'}
    ret={}
    for i in range(1, 5):
        if i in ret_data:
            ret[code_map[i]] = data2html(ret_data[i])
        else:
            ret[code_map[i]]={'hot':[]}
    print(ret)
    return ret

def no5_news_only_search(actor1,actor2,event,start,end):
    #方案五，先查询事件数据库，再找回新闻本身，统计热度图
    #输入多了一个事件
    #输出需要data2html的过滤
    # actor1 = ["", "USA"]
    # actor2 = ["China", ""]
    # event = [1, 2]
    sent_set=set()
    for event_code in event:
        # 循环搜索quadclass
        cnt = 0
        total_length = len(actor1)
        while cnt < total_length:
            # 对于每一对actor做一次查询，统计出现的次数
            dict = {'actor1name': actor1[cnt], 'actor2name': actor2[cnt], 'quadclass': event_code,
                    'sqldate': {'$gte': start, '$lte': end}}
            print(dict)
            res = events_tracking.find(dict)
            for item in res:
                #获取sentid,存入SET中，便于统计新闻数据
                sent_set.add(senid2index(item['sentid'])[0])
            cnt += 1
    sent_list=list(sent_set)
    #print(sent_list)

    #构造返回数据的字典，时间值
    start_int = timestr2stamp10(start)
    end_int = timestr2stamp10(end)
    ret_data = {start: 0}
    begin = start_int + 86400
    while begin <= end_int:
        # 生成从START到END的日期，ret_data为返回数据
        time_tmp = time.strftime("%Y%m%d", time.localtime(begin))
        ret_data[time_tmp] = 0
        begin = begin + 86400
    #print(ret_data)

    # 获取原新闻数据
    res = origin.find({'story_id': {"$in": sent_list}})
    #print(res)

    while True:
        try:
            item=res.next()
            try:
                if 'o_gt' in item:
                    # 查看原文时间
                    time_tmp = time.strftime("%Y%m%d", time.localtime(item['o_gt']))
                    if time_tmp in ret_data:
                        # 若时间在搜索范围内
                        ret_data[time_tmp] += 1
            except:
                continue
        except StopIteration:
            print('finished')
            break
        except Exception as e:
            print(e)

    ret_data = data2html(ret_data)
    print(ret_data)
    return ret_data


def no6_news_only_search(actor1,actor2,event,start,end):
    #方案六，先查询事件数据库，再找GKG，统计国家事件数的统计
    #输入多了一个事件
    #最后经dict_sort过滤
    # actor1 = ["", "USA"]
    # actor2 = ["China", ""]
    # event = [1, 2]
    sent_set=set()
    for event_code in event:
        # 循环搜索quadclass
        cnt = 0
        total_length = len(actor1)
        while cnt < total_length:
            # 对于每一对actor做一次查询，统计出现的次数
            dict = {'actor1name': actor1[cnt], 'actor2name': actor2[cnt], 'quadclass': event_code,
                    'sqldate': {'$gte': start, '$lte': end}}
            print(dict)
            res = events_tracking.find(dict)
            for item in res:
                #获取sentid,存入SET中，便于统计新闻数据
                sent_set.add(senid2index(item['sentid'])[0])
            cnt += 1
    sent_list=list(sent_set)
    #print(sent_list)

    ret_data={}

    # 获取原新闻数据
    res = origin.find({'story_id': {"$in": sent_list}})
    #print(res)

    while True:
        try:
            item=res.next()
            try:
                if 'gkg' in item and 'locations' in item['gkg']:
                    # 查看gkg.locations
                    if item['gkg']['locations']!="":
                        #print(item['gkg']['locations'])
                        location_list=gkg_country_extract(item['gkg']['locations'])
                        #print(location_list)
                        for country in location_list:
                            if country in ret_data:
                                ret_data[country]+=1
                            else:
                                ret_data[country]=1
            except:
                continue
        except StopIteration:
            print('finished')
            break
        except Exception as e:
            print(e)

    #将ret_data中的国家代号映射为中文
    country_data={}
    for key in ret_data:
        if key in country_dict:
            country_data[country_dict[key]]=ret_data[key]
    ret_data=dict_sort(country_data,10)
    #print(ret_data)

    #将国家名和热度值分开，使之适应前端输入
    ret={'hot':[],'country':[]}
    for item in ret_data:
        ret['country'].append(item[0])
        ret['hot'].append(item[1])
    print(ret)
    return ret

def no7_news_only_search(actor1,actor2,start,end):
    #方案七，先查询GKG（根据事件查新闻找GKG部分，再判断GKG中的persons是否包含人名，再返回相关地名
    #输入与no1相同,返回前10位地名及出现次数

    # actor1 = ['Miller', 'Donald Trump']
    # actor2 = ['Trump', 'Trump']
    # data = no7_news_only_search(actor1, actor2, "20180330", "20180515")
    ret_data = {}

    dict={"o_gt":{"$gte":timestr2stamp10(start),"$lte":timestr2stamp10(end)}}

    print(dict)
    cnt=0
    total=len(actor1)
    res=origin.find(dict).limit(2000)
    while True:
        try:
            item=res.next()
            try:
                if 'gkg' in item and 'persons' in item['gkg']:
                    #查看item['gkg']['persons'] 查看是否包含提供人名
                    if item['gkg']['persons']!="":
                        name_set=set(gkg_person_list(item['gkg']['persons'])) #转换为SET方便判断
                        #print(name_set)
                        cnt=0
                        while cnt<total:
                            if actor1[cnt] in name_set and actor2[cnt] in name_set:
                                #GKG中包含两个人名，可以统计地理信息了,同方案6的部分
                                if item['gkg']['locations'] != "":
                                    # print(item['gkg']['locations'])
                                    location_list = gkg_country_extract(item['gkg']['locations'])
                                    # print(location_list)
                                    for country in location_list:
                                        if country in ret_data:
                                            ret_data[country] += 1
                                        else:
                                            ret_data[country] = 1
                                break
                            cnt+=1
            except:
                continue
        except StopIteration:
            print('finished')
            break
        except Exception as e:
            print(e)

    # 将ret_data中的国家代号映射为中文
    country_data = {}
    for key in ret_data:
        if key in country_dict:
            country_data[country_dict[key]] = ret_data[key]
    ret_data = dict_sort(country_data, 10)

    #转换为适合前端展示的页面
    name = []
    value = []
    for item in ret_data:
        name.append(item[0])
        value.append(item[1])
    ret_data={}
    ret_data['hot']=value
    ret_data['country']=name
    print(ret_data)
    return ret_data

def no8_news_only_search(actor1, actor2, start, end):
    # 方案八，先查询GKG（根据事件查新闻找GKG部分，再判断GKG中的persons是否包含人名，之后查找英文新闻，统计热度

    # actor1=['Miller','Donald Trump']
    # actor2=['Trump','Trump']
    # data=no8_news_only_search(actor1,actor2,"20180330","20180515")


    # 问题在于： 前后端调用的start与end比直接用字符串生成的时间快8个小时,用DJANGO和直接跑文件，产生的时间不一样？？？
    # 根据时间统计热度，先按照时间戳生成要返回时间的字典
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

    dict = {"o_gt": {"$gte": start_int , "$lte": end_int}}

    print(dict)
    cnt = 0
    total = len(actor1)
    res = origin.find(dict).limit(2000)
    while True:
        try:
            item = res.next()
            try:
                if 'gkg' in item and 'persons' in item['gkg']:
                    # 查看item['gkg']['persons'] 查看是否包含提供人名
                    if item['gkg']['persons'] != "":
                        name_set = set(gkg_person_list(item['gkg']['persons']))  # 转换为SET方便判断
                        # print(name_set)
                        cnt = 0
                        while cnt < total:
                            if actor1[cnt] in name_set and actor2[cnt] in name_set:
                                # GKG中包含两个人名，之后查看英文新闻，统计热度

                                #再判断英文新闻是否有这两个词
                                res1 = re.search(actor1[cnt], item['s_cont'])
                                res2 = re.search(actor2[cnt], item['s_cont'])
                                if res1 is not None and res2 is not None:
                                    time_tmp = time.strftime("%Y%m%d", time.localtime(item['o_gt']))
                                    if time_tmp in ret_data:
                                        ret_data[time_tmp] += 1
                                break
                            cnt += 1
            except:
                continue
        except StopIteration:
            print('finished')
            break
        except Exception as e:
            print(e)

    #最后要经过data2html过滤，方便前端时间图的展示
    ret_data=data2html(ret_data)
    print(ret_data)
    return ret_data

def no9_news_only_search(actor1, actor2, start, end):
    # 方案九，先查询GKG（根据事件查新闻找GKG部分，再判断GKG中的persons是否包含人名，之后查找事件数据，统计人物出现次数前10位
    # 最后要经过字典排序与处理，返回前10位


    # actor1 = ['Miller', 'Donald Trump']
    # actor2 = ['Trump', 'Trump']
    # data = no9_news_only_search(actor1, actor2, "20180330", "20180515")

    ret_data = {}

    dict = {"o_gt": {"$gte": timestr2stamp10(start), "$lte": timestr2stamp10(end)}}

    print(dict)
    cnt = 0
    total = len(actor1)
    res = origin.find(dict).limit(2000)
    while True:
        try:
            item = res.next()
            try:
                if 'gkg' in item and 'persons' in item['gkg']:
                    # 查看item['gkg']['persons'] 查看是否包含提供人名
                    if item['gkg']['persons'] != "":
                        name_set = set(gkg_person_list(item['gkg']['persons']))  # 转换为SET方便判断
                        # print(name_set)
                        cnt = 0
                        while cnt < total:
                            if actor1[cnt] in name_set and actor2[cnt] in name_set:
                                # GKG中包含两个人名，查看事件数据，统计人物出现次数
                                event_cnt=0
                                while str(event_cnt) in item['events']:
                                    #遍历每个事件中的actor1name,actor2name
                                    name1=item['events'][str(event_cnt)]['actor1name']
                                    name2=item['events'][str(event_cnt)]['actor2name']
                                    if name1!="":
                                        if name1 not in ret_data:
                                            ret_data[name1]=1
                                        else:
                                            ret_data[name1]+=1
                                    if name2!="":
                                        if name2 not in ret_data:
                                            ret_data[name2]=1
                                        else:
                                            ret_data[name2]+=1
                                    event_cnt+=1
                                break
                            cnt += 1
            except:
                continue
        except StopIteration:
            print('finished')
            break
        except Exception as e:
            print(e)

    ret_data=dict_sort(ret_data,10)
    name=[]
    hot=[]
    for item in ret_data:
        name.append(item[0])
        hot.append(item[1])

    ret_data={}
    ret_data['name']=name
    ret_data['hot']=hot
    print(ret_data)
    return ret_data

actor1 = ['Xi Jinping', 'Donald Trump']
actor2 = ['Trump', 'Trump']
#data=no1_news_only_search(actor1,actor2,"20180506","20180515",num=2000)


#data=no2_news_only_search(actor1,actor2,"20180506","20180515")
#data=no2_news_only_search(actor1,actor2,"20180506","20180515")
#print(data2html(data))
#print(time.strftime("%Y%m%d",time.localtime(1495545426)))
#print(data)



#data=no3_news_only_search(actor1,actor2,"20180506","20180515")
#print(data)

#data=no4_news_only_search(actor1,actor2,event,"20180401","20181030")
#print(data)

#data=no5_news_only_search(actor1,actor2,event,"20180506","20180515")
#data=data2html(data)

# #data=no6_news_only_search(actor1,actor2,event,"20180506","20180508")
# actor1=['Miller','Donald Trump']
# actor2=['Trump','Trump']
#data=no9_news_only_search(actor1,actor2,"20180330","20180515")

#{'o_gt': {'$gte': 1522368000, '$lte': 1526342400}}
#{'o_gt': {'$gte': 1522339200, '$lte': 1526313600}}
#create_time_dict("20180501","20180515")