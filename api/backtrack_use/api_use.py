import time
import re
from api.backtrack_use.mongodb_link import origin,events_tracking
from api.backtrack_use.event_basic_use import *
import json
#from progressbar import *
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

    #pbar = ProgressBar().start()
    while True:
        try:
            item=res.next()
            try:
                if 's_cont' in item and 'o_gt' in item:
                    # 查看原文，统计出现次数
                    cnt=0
                    while cnt<total:
                        # 查询文章中是否出现了这两个人名
                        res1 = re.search(actor1[cnt], item['s_cont'])
                        res2 = re.search(actor2[cnt], item['s_cont'])
                        if res1 is not None and res2 is not None:
                            #若两个任命都有，将出现时间的热度加一
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

    #pbar.finish()
    ret_data=one_hot2target(ret_data)
    print(ret_data)
    return ret_data

def no2_news_only_search(actor1,actor2,start,end,num=0):
    #方案二，先查询英文新闻，再联立事件数据库，返回热度图
    #输入输出与no1相同,返回的数据需要经过data2html转化为前端接受的格式

    ret_data = create_time_dict(start, end)

    dict={"o_gt":{"$gte":timestr2stamp10(start),"$lte":timestr2stamp10(end)}}
    print(dict)
    cnt=0
    total=len(actor1)
    if num==0:
        res = origin.find(dict)
    else:
        res=origin.find(dict).limit(num)
    while True:
        try:
            item=res.next()
            try:
                if 's_cont' in item and 'o_gt' in item:
                    # 查询文章中是否出现了这两个人名
                    cnt=0
                    while cnt<total:
                        res1 = re.search(actor1[cnt], item['s_cont'])
                        res2 = re.search(actor2[cnt], item['s_cont'])
                        if res1 is not None and res2 is not None:
                            #若包含两个人名，统计事件数据库中的事件个数
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
    ret_data=one_hot2target(ret_data)
    print(ret_data)
    return ret_data


def no3_news_only_search(actor1,actor2,start,end,num=0,top=10):
    #方案三，先查询英文新闻，再联立GKG数据库，返回人物图
    #输入与no1相同,返回前TOP位人物及出现次数,默认是10
    #返回的是前10位的排名数据，KEY和VALUE分开
    ret_data = {}

    dict={"o_gt":{"$gte":timestr2stamp10(start),"$lte":timestr2stamp10(end)}}

    print(dict)
    cnt=0
    total=len(actor1)

    if num==0:
        res=origin.find(dict)
    else:
        res = origin.find(dict).limit(num)
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
                            #若包含两个人名，统计GKG数据库中的persons个数
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

    #将字典排序，取出前top位
    ret_data=dict_sort(ret_data,top)
    #将数据整合成适合前端输入的形式
    ret_data=rankdata(ret_data,'person','hot')

    print(ret_data)
    return ret_data

def no3_news_hot_search(actor1,actor2,start,end,num=0):
    #方案三的热度图版本，先查询英文新闻，再联立GKG数据库，返回事件热度图
    #输入与no1相同
    #返回的是前10位的排名数据，KEY和VALUE分开
    ret_data = create_time_dict(start, end)

    dict={"o_gt":{"$gte":timestr2stamp10(start),"$lte":timestr2stamp10(end)}}

    print(dict)
    cnt=0
    total=len(actor1)

    if num==0:
        res=origin.find(dict)
    else:
        res = origin.find(dict).limit(num)
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
                            #若包含两个人名，统计GKG数据库中的事件个数
                            time_tmp=time.strftime("%Y%m%d",time.localtime(item['o_gt']))
                            if time_tmp in ret_data:
                                #若gkg counts为空
                                if item['gkg']['counts']=='':
                                    ret_data[time_tmp]+=1
                                else:
                                    ret_data[time_tmp]+=gkg_counts_total(item['gkg']['counts'])
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
    ret_data=one_hot2target(ret_data)
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

def no4_news_hot_search(actor1,actor2,event,start,end):
    #热度版方案4，返回时间轴热度图
    #event为list，对应查询数据库的eventrootcode字段
    # actor1 = ["China", "China", "Japan", "", "USA"]
    # actor2 = ["USA", "Trump", "USA", "China", ""]
    # event = [1, 2, 3, 14, 19]
    ret_data={}
    time_dict=create_time_dict(start,end)
    data = {'time':[],'legend':[],'data':[]}
    tmp_dict={'name':'','type':'line','smooth':'true','data':[]}
    total_length=len(actor1)
    total_event=0
    for event_code in event:
        #循环搜索eventrootcode

        data['legend'].append(event_code_map_reverse[event_code])
        tmp_dict={'name':'','type':'line','smooth':'true','data':[]}
        tmp_dict['name']=event_code_map_reverse[event_code]
        tmp_dict['data']=create_time_dict(start,end)
        cnt=0
        while cnt<total_length:
            #对于每一对actor做一次查询，统计出现的次数
            dict={'actor1name':actor1[cnt],'actor2name':actor2[cnt],'eventrootcode':event_code,'sqldate':{'$gte':start,'$lte':end}}
            print(dict)
            res=events_tracking.find(dict)
            for item in res:
                if 'sqldate' in item:
                    tmp_dict['data'][item['sqldate']]+=1
            cnt+=1
        print(tmp_dict)
        data['data'].append(tmp_dict)
        total_event+=1
    #按照eventrootcode依此进行类型转换，以适应前端输入格式
    start_int = timestr2stamp10(start)
    end_int = timestr2stamp10(end)
    begin = start_int + 86400
    while begin <= end_int:
        # 生成从START到END的日期，ret_data为返回数据
        time_tmp = time.strftime("%Y%m%d", time.localtime(begin))
        begin = begin + 86400
        data['time'].append(time_tmp)
    cnt=0
    for item in data['data']:
        #print(item['data'])
        tmp_list=[]
        for key in item['data']:
            tmp_list.append(item['data'][key])
        data['data'][cnt]['data']=tmp_list
        cnt+=1
    print(data)
    return data
# actor1 = [ "", "USA"]
# actor2 = [ "China", ""]
# event = [1, 2, 3]
# no4_news_hot_search(actor1,actor2,event,"20180401","20180410")
# {'time': ['20180402', '20180403', '20180404', '20180405', '20180406', '20180407', '20180408', '20180409', '20180410'],
# 'legend': ['官方声明', '呼吁', '表达合作意向'], 'data': [
# {'name': '官方声明', 'type': 'line', 'smooth': 'true', 'data': [2, 34, 38, 51, 21, 12, 0, 0, 0, 1]},
# {'name': '呼吁', 'type': 'line', 'smooth': 'true', 'data': [0, 1, 3, 10, 5, 12, 0, 0, 0, 0]},
# {'name': '表达合作意向', 'type': 'line', 'smooth': 'true', 'data': [5, 27, 30, 23, 20, 25, 0, 0, 0, 0]}]}

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
    ret_data = create_time_dict(start, end)
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

def no5_news_hot_search(actor1,actor2,event,start,end):
    #方案五的热度图实现，先查询事件数据库，再找回新闻本身，统计热度图
    #event是基于eventrootcode查询
    #输出需要data2html的过滤
    # actor1 = ["", "USA"]
    # actor2 = ["China", ""]
    # event = [1, 2]
    sent_set=set()
    for event_code in event:
        # 循环搜索eventrootcode
        cnt = 0
        total_length = len(actor1)
        while cnt < total_length:
            # 对于每一对actor做一次查询，统计出现的次数
            dict = {'actor1name': actor1[cnt], 'actor2name': actor2[cnt], 'eventrootcode': event_code,
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
    ret_data = create_time_dict(start, end)
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
    ret_data=one_hot2target(ret_data)
    print(ret_data)
    return ret_data

def no6_news_only_search(actor1,actor2,event,start,end,top):
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

    # 将ret_data中的国家代号映射为中文
    country_data={}
    for key in ret_data:
        if key in country_dict:
            country_data[country_dict[key]]=ret_data[key]
    # 将字典排序，取出前top位
    ret_data = dict_sort(country_data, top)
    # 将数据整合成适合前端输入的形式
    ret_data = rankdata(ret_data, 'country', 'hot')


    print(ret_data)
    return ret_data

def no6_news_hot_search(actor1,actor2,event,start,end):
    #方案六的热度，先查询事件数据库，再找GKG中counts的时间数目，返回时间轴热度图
    #event基于eventrootcode
    # actor1 = ["", "USA"]
    # actor2 = ["China", ""]
    # event = [1, 2]
    sent_set=set()
    for event_code in event:
        # 循环搜索eventrootcode
        cnt = 0
        total_length = len(actor1)
        while cnt < total_length:
            # 对于每一对actor做一次查询，统计出现的次数
            dict = {'actor1name': actor1[cnt], 'actor2name': actor2[cnt], 'eventrootcode': event_code,
                    'sqldate': {'$gte': start, '$lte': end}}
            print(dict)
            res = events_tracking.find(dict)
            for item in res:
                #获取sentid,存入SET中，便于统计新闻数据
                sent_set.add(senid2index(item['sentid'])[0])
            cnt += 1
    sent_list=list(sent_set)
    #print(sent_list)

    ret_data = create_time_dict(start, end)

    # 获取原新闻数据
    res = origin.find({'story_id': {"$in": sent_list}})
    #print(res)

    while True:
        try:
            item=res.next()
            try:
                if 'gkg' in item and 'counts' in item['gkg']:
                    # 查看gkg.counts，统计事件个数
                    time_tmp=time.strftime("%Y%m%d",time.localtime(item['o_gt']))
                    if time_tmp in ret_data:
                        #若gkg counts为空
                            if item['gkg']['counts']=='':
                                ret_data[time_tmp]+=1
                            else:
                                ret_data[time_tmp]+=gkg_counts_total(item['gkg']['counts'])
            except:
                continue
        except StopIteration:
            print('finished')
            break
        except Exception as e:
            print(e)

    ret_data=data2html(ret_data)
    ret_data=one_hot2target(ret_data)
    print(ret_data)
    return ret_data

def no7_news_only_search(actor1,actor2,start,end,top,num=0):
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
    if num==0:
        res = origin.find(dict)
    else:
        res=origin.find(dict).limit(num)
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
    # 将字典排序，取出前top位
    ret_data = dict_sort(country_data, top)
    # 将数据整合成适合前端输入的形式
    ret_data = rankdata(ret_data, 'name', 'hot')
    print(ret_data)
    return ret_data

def no7_news_hot_search(actor1,actor2,start,end,num=0):
    #方案七热度图实现，先查询GKG（根据事件查新闻找GKG部分，再判断GKG中的persons是否包含人名，返回事件热度图

    # actor1 = ['Miller', 'Donald Trump']
    # actor2 = ['Trump', 'Trump']
    # data = no7_news_only_search(actor1, actor2, "20180330", "20180515")
    ret_data = create_time_dict(start, end)

    dict={"o_gt":{"$gte":timestr2stamp10(start),"$lte":timestr2stamp10(end)}}

    print(dict)
    cnt=0
    total=len(actor1)
    if num==0:
        res = origin.find(dict)
    else:
        res=origin.find(dict).limit(num)
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
                                #GKG中包含两个人名，统计gkg counts的热度
                                time_tmp=time.strftime("%Y%m%d",time.localtime(item['o_gt']))
                                if time_tmp in ret_data:
                                    #若gkg counts为空
                                    if item['gkg']['counts']=="":
                                        ret_data[time_tmp]+=1
                                    else:
                                        ret_data[time_tmp]+=gkg_counts_total(item['gkg']['counts'])
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
    ret_data=one_hot2target(ret_data)
    print(ret_data)
    return ret_data

def no8_news_only_search(actor1, actor2, start, end,num=0):
    # 方案八，先查询GKG（根据事件查新闻找GKG部分，再判断GKG中的persons是否包含人名，之后查找英文新闻，统计热度

    # actor1=['Miller','Donald Trump']
    # actor2=['Trump','Trump']
    # data=no8_news_only_search(actor1,actor2,"20180330","20180515")


    # 问题在于： 前后端调用的start与end比直接用字符串生成的时间快8个小时,用DJANGO和直接跑文件，产生的时间不一样？？？
    # 根据时间统计热度，先按照时间戳生成要返回时间的字典
    ret_data=create_time_dict(start,end)

    dict = {"o_gt": {"$gte": timestr2stamp10(start), "$lte": timestr2stamp10(end)}}

    print(dict)
    cnt = 0
    total = len(actor1)
    if num==0:
        res = origin.find(dict)
    else:
        res=origin.find(dict).limit(num)
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
    ret_data=one_hot2target(ret_data)
    print(ret_data)
    return ret_data

def no9_news_only_search(actor1, actor2, start, end,top,num=0):
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
    if num==0:
        res = origin.find(dict)
    else:
        res=origin.find(dict).limit(num)
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

    # 将字典排序，取出前top位
    ret_data = dict_sort(ret_data, top)
    # 将数据整合成适合前端输入的形式
    ret_data = rankdata(ret_data, 'name', 'hot')
    print(ret_data)
    return ret_data

def no9_news_hot_search(actor1, actor2, start, end,num=0):
    # 方案九热度图实现，先查询GKG（根据事件查新闻找GKG部分，再判断GKG中的persons是否包含人名，之后查找事件数据，统计人物时间热度图

    # actor1 = ['Miller', 'Donald Trump']
    # actor2 = ['Trump', 'Trump']
    # data = no9_news_only_search(actor1, actor2, "20180330", "20180515")

    ret_data=create_time_dict(start,end)

    dict = {"o_gt": {"$gte": timestr2stamp10(start), "$lte": timestr2stamp10(end)}}

    print(dict)
    cnt = 0
    total = len(actor1)
    if num==0:
        res = origin.find(dict)
    else:
        res=origin.find(dict).limit(num)
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
                                # GKG中包含两个人名，查看事件数据，统计事件热度
                                event_cnt=0
                                while str(event_cnt) in item['events']:
                                    event_cnt+=1
                                time_tmp = time.strftime("%Y%m%d", time.localtime(item['o_gt']))
                                if time_tmp in ret_data:
                                    ret_data[time_tmp] += event_cnt
                                break
                            cnt += 1
            except:
                continue
        except StopIteration:
            print('finished')
            break
        except Exception as e:
            print(e)
    ret_data=data2html(ret_data)
    ret_data=one_hot2target(ret_data)
    print(ret_data)
    return ret_data

# actor1 = ['Xi Jinping', 'China']
# actor2 = ['Trump', 'USA']

#data=no1_news_only_search(actor1,actor2,"20180401","20180420",num=2000)

#data=no2_news_only_search(actor1,actor2,"20180506","20180515",num=2000)

#data=no3_news_only_search(actor1,actor2,"20180506","20180515",num=2000,top=11)

actor1 = ['Xi Jinping', 'China','Xi','China','Jinping Xi','China','']
actor2 = ['Trump', 'USA','Trump','United States','Donald Trump','','USA']
event=[1,2,3,4]

#data=no4_news_only_search(actor1,actor2,event,"20180401","20180430")
#print(data)

#data=no5_news_only_search(actor1,actor2,event,"20180401","20180430")


#data=no6_news_only_search(actor1,actor2,event,"20180401","20180430",10)
# actor1=['Miller','Donald Trump']
# actor2=['Trump','Trump']
#data=no7_news_only_search(actor1,actor2,"20180330","20180515",16,2000)

#data=no8_news_only_search(actor1,actor2,"20180330","20180515",2000)

#data=no9_news_only_search(actor1,actor2,"20180330","20180515",16,2000)
#{'o_gt': {'$gte': 1522368000, '$lte': 1526342400}}
#{'o_gt': {'$gte': 1522339200, '$lte': 1526313600}}
#create_time_dict("20180501","20180515")
dict={}
#with open('data.txt','r') as f:
with open('api/backtrack_use/data.txt','r') as f:
    dict=json.loads(f.read())

actor1 = ["China", "China", "Japan", "", "USA"]
actor2 = ["USA", "Trump", "USA", "China", ""]
event = [1, 2, 3, 14, 19]
#no4_news_hot_search(actor1,actor2,event,"20180401","20180430")
#方案4执行结果格式
"""
ret4={'官方声明': {'hot': [[1522512000000, 2], [1522598400000, 34], [1522684800000, 38], [1522771200000, 51], [1522857600000, 21], [1522944000000, 12], [1523289600000, 1], [1523980800000, 1], [1524067200000, 14], [1524153600000, 13], [1524240000000, 5], [1524326400000, 4], [1524412800000, 15], [1524499200000, 14], [1524585600000, 38], [1524672000000, 6], [1524758400000, 10], [1524844800000, 9], [1524931200000, 12], [1525017600000, 7]], 'max_value': 51, 'min_value': 0},
      '呼吁': {'hot': [[1522598400000, 1], [1522684800000, 3], [1522771200000, 10], [1522857600000, 5], [1522944000000, 12], [1524067200000, 3], [1524153600000, 1], [1524412800000, 1], [1524585600000, 1], [1524672000000, 1], [1524758400000, 2], [1524844800000, 1], [1525017600000, 3]], 'max_value': 12, 'min_value': 0}, 
      '表达合作意向': {'hot': [[1522512000000, 5], [1522598400000, 27], [1522684800000, 30], [1522771200000, 23], [1522857600000, 20], [1522944000000, 25], [1523980800000, 2], [1524067200000, 4], [1524153600000, 18], [1524240000000, 26], [1524326400000, 9], [1524412800000, 12], [1524499200000, 16], [1524585600000, 24], [1524672000000, 34], [1524758400000, 31], [1524844800000, 5], [1524931200000, 27], [1525017600000, 12]], 'max_value': 34, 'min_value': 0}, 
      '商议': {'hot': []}, '从事外交合作': {'hot': []}, '开展物质合作': {'hot': []}, '提供援助': {'hot': []}, '不再反对': {'hot': []}, '调查': {'hot': []}, '询问': {'hot': []}, '反对': {'hot': []}, '拒绝': {'hot': []}, '威胁': {'hot': []}, 
      '抗议': {'hot': [[1522684800000, 3], [1522771200000, 1], [1523980800000, 1], [1524672000000, 1]], 'max_value': 3, 'min_value': 0}, 
      '展现武力': {'hot': []}, '减少联系': {'hot': []}, '逼迫': {'hot': []}, '攻击': {'hot': []}, 
      '战斗': {'hot': [[1522512000000, 2], [1522598400000, 1], [1522684800000, 7], [1522771200000, 5], [1522857600000, 6], [1522944000000, 1], [1523462400000, 1], [1524067200000, 51], [1524153600000, 65], [1524240000000, 42], [1524326400000, 53], [1524412800000, 111], [1524499200000, 95], [1524585600000, 64], [1524672000000, 62], [1524758400000, 35], [1524844800000, 17], [1524931200000, 3], [1525017600000, 6]], 'max_value': 111, 'min_value': 0}, 'null': {'hot': []}}
"""
#no5_news_hot_search(actor1,actor2,event,"20180401","20180430")
#方案5执行结果格式
"""
ret5={'hot': [[1522512000000, 6], [1522598400000, 38], [1522684800000, 73], [1522771200000, 86], [1522857600000, 53], [1522944000000, 65], [1523030400000, 0], [1523116800000, 0], [1523203200000, 0], 
[1523289600000, 0], [1523376000000, 0], [1523462400000, 0], [1523548800000, 0], [1523635200000, 0], [1523721600000, 0], [1523808000000, 0], [1523894400000, 0], [1523980800000, 0], [1524067200000, 6], 
[1524153600000, 53], [1524240000000, 29], [1524326400000, 35], [1524412800000, 36], [1524499200000, 57], [1524585600000, 58], [1524672000000, 53], [1524758400000, 37], [1524844800000, 25], 
[1524931200000, 23], [1525017600000, 23]], 'max_value': 86, 'min_value': 0}
"""
#no6_news_hot_search(actor1,actor2,event,"20180401","20180430")
#方案6行结果格式
"""
ret6={'hot': [[1522512000000, 6], [1522598400000, 38], [1522684800000, 73], [1522771200000, 86], [1522857600000, 53], [1522944000000, 65], [1523030400000, 0], [1523116800000, 0], [1523203200000, 0], 
[1523289600000, 0], [1523376000000, 0], [1523462400000, 0], [1523548800000, 0], [1523635200000, 0], [1523721600000, 0], [1523808000000, 0], [1523894400000, 0], [1523980800000, 0], [1524067200000, 6], 
[1524153600000, 53], [1524240000000, 29], [1524326400000, 35], [1524412800000, 36], [1524499200000, 57], [1524585600000, 58], [1524672000000, 53], [1524758400000, 37], [1524844800000, 25], 
[1524931200000, 23], [1525017600000, 23]], 'max_value': 86, 'min_value': 0}
"""


actor1 = ['Miller', 'Donald Trump']
actor2 = ['Trump', 'Trump']
#data = no7_news_hot_search(actor1, actor2, "20180330", "20180515",2000)
"""
ret7={'hot': [[1522339200000, 55], [1522425600000, 0], [1522512000000, 0], [1522598400000, 0], [1522684800000, 0], [1522771200000, 0], [1522857600000, 0], 
[1522944000000, 0], [1523030400000, 0], [1523116800000, 0], [1523203200000, 0], [1523289600000, 0], [1523376000000, 0], [1523462400000, 0], [1523548800000, 0], 
[1523635200000, 0], [1523721600000, 0], [1523808000000, 0], [1523894400000, 0], [1523980800000, 0], [1524067200000, 0], [1524153600000, 0], [1524240000000, 0],
 [1524326400000, 0], [1524412800000, 0], [1524499200000, 0], [1524585600000, 0], [1524672000000, 0], [1524758400000, 0], [1524844800000, 0], [1524931200000, 0], 
 [1525017600000, 0], [1525104000000, 0], [1525190400000, 0], [1525276800000, 0], [1525363200000, 0], [1525449600000, 0], [1525536000000, 0], [1525622400000, 0],
  [1525708800000, 0], [1525795200000, 0], [1525881600000, 0], [1525968000000, 0], [1526054400000, 0], [1526140800000, 0], [1526227200000, 0], [1526313600000, 0]],
  'max_value': 55, 'min_value': 0}
"""
#data=no8_news_only_search(actor1,actor2,"20180330","20180410",2000)
"""
ret8={'hot': [[1522339200000, 55], [1522425600000, 0], [1522512000000, 0], [1522598400000, 0], [1522684800000, 0], [1522771200000, 0], [1522857600000, 0], 
[1522944000000, 0], [1523030400000, 0], [1523116800000, 0], [1523203200000, 0], [1523289600000, 0]], 'max_value': 55, 'min_value': 0}
"""
#data=no9_news_hot_search(actor1,actor2,"20180330","20180410",2000)
"""
ret9={'hot': [[1522339200000, 197], [1522425600000, 0], [1522512000000, 0], [1522598400000, 0], [1522684800000, 0], [1522771200000, 0], [1522857600000, 0], 
[1522944000000, 0], [1523030400000, 0], [1523116800000, 0], [1523203200000, 0], [1523289600000, 0]], 'max_value': 197, 'min_value': 0}
"""