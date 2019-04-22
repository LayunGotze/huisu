import time
import re
from api.backtrack_use.mongodb_link import *
from api.backtrack_use.event_basic_use import *
import json

"""
事件回溯9个方案所需要的接口函数
每个函数输入相关信息，进行查询统计，返回前端可展示的数据
所用到的基本函数可见api.backtrack_use.event_basic_use
"""

def news_search(actor1, actor2, start, end, num=0):
    # 方案1-3的统一解决方案
    ret_data = create_time_dict(start, end)
    msg = "回溯成功"
    story_id_set = set()
    dict = {"s_pt": {"$gte": timestr2stamp10(start), "$lte": timestr2stamp10(end)}}
    print(dict)
    cnt = 0
    total = len(actor1)
    if num == 0:
        res = origin.find(dict)
    else:
        res = origin.find(dict).limit(num)
    while True:
        try:
            item = res.next()
            try:
                if 's_cont' in item and 's_pt' in item and item['s_pt'] > 0:
                    # 查看原文，统计出现次数
                    cnt = 0
                    while cnt < total:
                        # 查询文章中是否出现了这两个人名
                        res1 = re.search(actor1[cnt], item['s_cont'])
                        res2 = re.search(actor2[cnt], item['s_cont'])
                        if res1 is not None and res2 is not None:
                            # 若两个人名都有，将出现时间的热度加一,方案1
                            time_tmp = time.strftime("%Y%m%d", time.localtime(item['s_pt']))
                            if time_tmp in ret_data:
                                ret_data[time_tmp] += 1

                            story_id_set.add(item['story_id'])
                            break
                        cnt += 1
            except:
                continue
        except StopIteration:
            print('finished')
            break
        except Exception as e:
            print(e)
    ret_data = one_hot2target(data2html(ret_data))
    story_id_list = list(story_id_set)
    #print(ret_data)
    if len(story_id_list)==0:
        msg = "未回溯到数据"
    # 方案2，3，找回gkg和event
    event_res = events.find({'story_id': {'$in': story_id_list}})
    gkg_res = gkg.find({'gkgrecordid': {'$in': story_id_list}})

    ret_data_event = create_time_dict(start, end)
    ret_data_gkg = create_time_dict(start, end)
    for item in event_res:
        #方案2
        if 'dateadded' in item and item['dateadded'] in ret_data_event and 'nummentions' in item:
                ret_data_event[item['dateadded']] += int(item['nummentions'])
    for item in gkg_res:
        # 方案3
        if 'date' in item and item['date'][0:8] in ret_data_gkg:
            ret_data_gkg[item['date'][0:8]] += 1

    ret_data_event = one_hot2target(data2html(ret_data_event))
    ret_data_gkg = one_hot2target(data2html(ret_data_gkg))
    #print(ret_data_event)
    #print(ret_data_gkg)

    ret = {'1': ret_data, '2': ret_data_event, '3': ret_data_gkg,'msg':msg}
    ret['1_all']=calculate_all(ret['1'])
    ret['2_all']=calculate_all(ret['2'])
    ret['3_all']=calculate_all(ret['3'])
    print(ret)
    return ret
actor1 = ["China"]
actor2 = ["Trump"]
event = [1, 2, 3, 14, 19]
#data=news_search(actor1,actor2,"20180401","20180430",num=2000)
#print(data)

def gkg_search(actor1, actor2, start, end, num=0):
    # 方案7-9的解决方案
    ret_data = create_time_dict(start, end)
    msg="回溯成功"
    dict = {"date": {"$gte": start, "$lte": end}}
    print(dict)
    cnt = 0
    total = len(actor1)
    if num == 0:
        res = gkg.find(dict)
    else:
        res = gkg.find(dict).limit(num)
    print(res.count())
    gkg_res_set = set()
    for item in res:
        if 'persons' in item and 'locations' in item and 'organizations' in item:
            name_set = set(gkg_person_list(item['persons']))  # 转换为SET方便判断
            location_set=set(gkg_location_list(item['locations']))
            organization_set=set(gkg_organization_list(item['organizations']))
            cnt = 0
            while cnt < total:
                if (actor1[cnt] in name_set and actor2[cnt] in name_set) or (actor1[cnt] in location_set and actor2[cnt] in location_set) or (actor1[cnt] in organization_set and actor2[cnt] in organization_set):
                    # GKG中包含两个人名，统计gkg counts的热度
                    time_tmp = item['date'][0:8]
                    print(time_tmp)
                    if time_tmp in ret_data:
                        # 若gkg counts为空
                        gkg_res_set.add(item['gkgrecordid'])
                        ret_data[time_tmp] += 1
                        """
                        if item['numarts'] == "":
                            ret_data[time_tmp] += 1
                        else:
                            ret_data[time_tmp] += item['numarts']
                        """
                    break
                cnt += 1

    ret_data = data2html(ret_data)
    ret_data = one_hot2target(ret_data)
    #print(ret_data)
    gkg_res_list = list(gkg_res_set)
    #print(gkg_res_list)
    if len(gkg_res_list)==0:
        msg = "未回溯到数据"
    news_res = origin.find({"story_id": {"$in": gkg_res_list}})

    # 方案8
    ret_data_news = create_time_dict(start, end)
    total = len(actor1)
    for item in news_res:
        if 's_pt' in item and item['s_pt']>0:
            # 查看原文，统计出现次数
            time_tmp = time.strftime("%Y%m%d", time.localtime(item['s_pt']))
            if time_tmp in ret_data_news:
                ret_data_news[time_tmp] += 1
    ret_data_news = one_hot2target(data2html(ret_data_news))
    print(ret_data_news)

    # 方案9
    event_res = events.find({"story_id": {"$in": gkg_res_list}})
    ret_data_event = create_time_dict(start, end)
    for item in event_res:
        if item['dateadded'] in ret_data_event and 'nummentions' in item:
            ret_data_event[item['dateadded']] +=int(item['nummentions'])
        #if item['dateadded'] in ret_data_event:
         #   ret_data_event[item['dateadded']] +=1
    ret_data_event = one_hot2target(data2html(ret_data_event))
    print(ret_data_event)

    ret = {'7': ret_data, '8': ret_data_news, '9': ret_data_event,'msg':msg}
    ret['7_all']=calculate_all(ret['7'])
    ret['8_all']=calculate_all(ret['8'])
    ret['9_all']=calculate_all(ret['9'])
    print(ret)
    return ret
# actor1=['Trump']
# actor2=['Trump']
# data=gkg_search(actor1,actor2,"20180401","20180430",num=10000)
# print(data)

def event_search(actor1, actor2, event_code_list, start, end, num=0):
    # 方案4-6的解决方案
    ret_data = {}
    msg="回溯成功"
    time_dict = create_time_dict(start, end)
    data = {'time': [], 'legend': [], 'data': []}
    tmp_dict = {'name': '', 'type': 'line', 'smooth': 'true', 'data': []}
    total_length = len(actor1)
    total_event = 0
    event_res_set = set()
    for event_code in event_code_list:
        # 循环搜索所有eventrootcode
        data['legend'].append(event_code_map_english[event_code])
        tmp_dict = {'name': '', 'type': 'line', 'smooth': 'true', 'data': []}
        tmp_dict['name'] = event_code_map_english[event_code]
        tmp_dict['data'] = create_time_dict(start, end)
        cnt = 0
        while cnt < total_length:
            # 对于每一对actor做一次查询，统计出现的次数
            dict = {'actor1name': actor1[cnt], 'actor2name': actor2[cnt], 'eventrootcode': event_code,
                    'dateadded': {'$gte': start, '$lte': end}}
            print(dict)
            res = events.find(dict)
            for item in res:
                if 'dateadded' in item and 'nummentions' in item:
                    tmp_dict['data'][item['dateadded']] += int(item['nummentions'])
                    event_res_set.add(item['story_id'])
            cnt += 1
        # 统计各小类事件的热度
        ret_data[event_code] = one_hot2target(data2html(tmp_dict['data']))
        total_event += 1

    ret = {'all': ret_data}
    ret['data'] = event_all_4_conclusion(ret_data)
    all = event_all_conclusion(ret['data'])
    ret['all'] = all
    # print(ret)
    event_res_list = list(event_res_set)
    # print(event_res_list)
    if len(event_res_set)==0:
        msg = "未回溯到数据"
    # 方案5
    news_res = origin.find({'story_id': {"$in": event_res_list}})
    ret_data_news = create_time_dict(start, end)
    total = len(actor1)
    for item in news_res:
        if 's_pt' in item and item['s_pt'] > 0:
            # 查看原文，统计出现次数
            time_tmp = time.strftime("%Y%m%d", time.localtime(item['s_pt']))
            if time_tmp in ret_data_news:
                ret_data_news[time_tmp] += 1
    ret_data_news = one_hot2target(data2html(ret_data_news))
    # print(ret_data_news)

    # 方案6
    gkg_res = gkg.find({'gkgrecordid': {"$in": event_res_list}})
    ret_data_gkg = create_time_dict(start, end)
    res = gkg.find({'gkgrecordid': {"$in": event_res_list}})
    gkg_res_set = set()
    total = len(actor1)
    for item in res:
        time_tmp = item['date'][0:8]
        if time_tmp in ret_data_gkg:
            ret_data_gkg[time_tmp] += 1

    ret_data_gkg = one_hot2target(data2html(ret_data_gkg))
    # print(ret_data_gkg)

    ret_data = {'4': ret, '5': ret_data_news, '6': ret_data_gkg,'msg':msg}
    cnt=0
    for item in ret_data['4']['data']['data']:
        for num in item['data']:
            cnt+=num
    ret_data['4_all']=cnt
    ret_data['5_all']=calculate_all(ret_data['5'])
    ret_data['6_all']=calculate_all(ret_data['6'])
    print(ret_data)
    return ret_data


def news_search_final(actor_all,actor_one,actor_null,start,end,num=0):
    # 方案1-3的统一解决方案
    ret_data = create_time_dict(start, end)
    msg = "回溯成功"
    story_id_set = set()
    dict = {"s_pt": {"$gte": timestr2stamp10(start), "$lte": timestr2stamp10(end)}}
    print(dict)
    cnt = 0
    if num == 0:
        res = origin.find(dict)
    else:
        res = origin.find(dict).limit(num)
    cnt=0
    print(res.count())
    while True:
        try:
            cnt += 1
            if cnt % 1000 == 0:
                print(cnt)
            item = res.next()
            try:
                if 's_cont' in item and 's_pt' in item:
                    if item['s_pt'] <= 0:
                        item['s_pt']=item['o_pt']
                    # 查看原文，统计出现次数
                    tmp=word_in_article_fullmatch(actor_all,actor_one,actor_null,item['s_cont'])
                    if tmp==1:
                        time_tmp = time.strftime("%Y%m%d", time.localtime(item['s_pt']))
                        if time_tmp in ret_data:
                            ret_data[time_tmp] += 1
                            story_id_set.add(item['story_id'])
            except:
                continue
        except StopIteration:
            print('finished')
            break
        except Exception as e:
            print(e)
    ret_data = one_hot2target(data2html(ret_data))
    story_id_list = list(story_id_set)
    #print(ret_data)
    if len(story_id_list)==0:
        msg = "未回溯到数据"
    # 方案2，3，找回gkg和event
    event_res = events.find({'story_id': {'$in': story_id_list}})
    gkg_res = gkg.find({'gkgrecordid': {'$in': story_id_list}})

    ret_data_event = create_time_dict(start, end)
    ret_data_gkg = create_time_dict(start, end)
    for item in event_res:
        #方案2
        if 'sqldate' in item and item['sqldate'] in ret_data_event and 'nummentions' in item:
                ret_data_event[item['sqldate']] += int(item['nummentions'])
    for item in gkg_res:
        # 方案3
        if 'date' in item and item['date'][0:8] in ret_data_gkg:
            ret_data_gkg[item['date'][0:8]] += 1

    ret_data_event = one_hot2target(data2html(ret_data_event))
    ret_data_gkg = one_hot2target(data2html(ret_data_gkg))
    #print(ret_data_event)
    #print(ret_data_gkg)

    ret = {'1': ret_data, '2': ret_data_event, '3': ret_data_gkg,'msg':msg}
    ret['1_all']=calculate_all(ret['1'])
    ret['2_all']=calculate_all(ret['2'])
    ret['3_all']=calculate_all(ret['3'])
    print(ret)
    return ret

def gkg_search_final(actor_all,actor_one,actor_null,start,end,num=0):
    ret_data = create_time_dict(start, end)
    msg="回溯成功"
    dict = {"date": {"$gte": start, "$lte": end}}
    print(dict)
    if num == 0:
        res = gkg.find(dict)
    else:
        res = gkg.find(dict).limit(num)
    gkg_res_set = set()
    cnt=0
    for item in res:
         cnt+=1
         if cnt%1000==0:
             print(cnt)
         if 'persons' in item and 'locations' in item and 'organizations' in item and 'allnames' in item:
            name_set = set(gkg_person_list(item['persons']))  # 转换为SET方便判断
            location_set=set(gkg_location_list(item['locations']))
            organization_set=set(gkg_organization_list(item['organizations']))
            allname_set=set(gkg_allnames_total(item['allnames']))
            final_set=name_set|location_set|organization_set|allname_set
            tmp=word_in_gkg(actor_all,actor_one,actor_null,final_set)
            if tmp==1 and 'date' in item:
                time_tmp = item['date'][0:8]
                if time_tmp in ret_data:
                    gkg_res_set.add(item['gkgrecordid'])
                    ret_data[time_tmp] += 1
    ret_data = data2html(ret_data)
    ret_data = one_hot2target(ret_data)
    print(ret_data)
    gkg_res_list = list(gkg_res_set)

    if len(gkg_res_list)==0:
        msg = "未回溯到数据"
    news_res = origin.find({"story_id": {"$in": gkg_res_list}})

    # 方案8
    ret_data_news = create_time_dict(start, end)

    for item in news_res:
        if 's_pt' in item:
            # 查看原文，统计出现次数
            if item['s_pt'] <= 0:
                item['s_pt'] = item['o_pt']
            time_tmp = time.strftime("%Y%m%d", time.localtime(item['s_pt']))
            if time_tmp in ret_data_news:
                ret_data_news[time_tmp] += 1
    ret_data_news = one_hot2target(data2html(ret_data_news))
    print(ret_data_news)

    # 方案9
    event_res = events.find({"story_id": {"$in": gkg_res_list}})
    ret_data_event = create_time_dict(start, end)
    for item in event_res:
        if item['sqldate'] in ret_data_event and 'nummentions' in item:
            ret_data_event[item['sqldate']] +=int(item['nummentions'])
        #if item['dateadded'] in ret_data_event:
         #   ret_data_event[item['dateadded']] +=1
    ret_data_event = one_hot2target(data2html(ret_data_event))
    print(ret_data_event)

    ret = {'7': ret_data, '8': ret_data_news, '9': ret_data_event,'msg':msg}
    ret['7_all']=calculate_all(ret['7'])
    ret['8_all']=calculate_all(ret['8'])
    ret['9_all']=calculate_all(ret['9'])
    print(ret)
    return ret

def event_search_final(actor1countrycode,actor1typecode,actor2countrycode,actor2typecode,event_list,location,start,end):
    ret_data = {}
    msg="回溯成功"
    time_dict = create_time_dict(start, end)
    data = {'time': [], 'legend': [], 'data': []}
    tmp_dict = {'name': '', 'type': 'line', 'smooth': 'true', 'data': []}
    total_event = 0
    event_res_set = set()
    
    search_list=[actor1countrycode,actor1typecode,actor2countrycode,actor2typecode,location]
    search_value=['actor1countrycode','actor1type1code','actor2countrycode','actor2type1code','actiongeo_countrycode']
    query_dict={'dateadded': {'$gte': start, '$lte': end}}
    for i in range(5):
        if search_list[i]!='':
            query_dict[search_value[i]]=search_list[i]
    for event_code in event_list:
        data['legend'].append(event_code_map_english[event_code])
        tmp_dict = {'name': '', 'type': 'line', 'smooth': 'true', 'data': []}
        tmp_dict['name'] = event_code_map_english[event_code]
        tmp_dict['data'] = create_time_dict(start, end)
        query_dict['eventrootcode']=event_code
        print(query_dict)
        res=events.find(query_dict)
        for item in res:
            if 'sqldate' in item and 'nummentions' in item and item['sqldate'] in tmp_dict['data']:
                tmp_dict['data'][item['sqldate']] += int(item['nummentions'])
                event_res_set.add(item['story_id'])
        ret_data[event_code] = one_hot2target(data2html(tmp_dict['data']))
    ret = {'all': ret_data}
    ret['data'] = event_all_4_conclusion(ret_data)
    all = event_all_conclusion(ret['data'])
    ret['all'] = all
    # print(ret)
    event_res_list = list(event_res_set)
    # print(event_res_list)
    if len(event_res_set)==0:
        msg = "未回溯到数据"
    # 方案5
    news_res = origin.find({'story_id': {"$in": event_res_list}})
    ret_data_news = create_time_dict(start, end)

    for item in news_res:
        if 's_pt' in item:
            # 查看原文，统计出现次数
            if item['s_pt'] <= 0:
                item['s_pt'] = item['o_pt']
            time_tmp = time.strftime("%Y%m%d", time.localtime(item['s_pt']))
            if time_tmp in ret_data_news:
                ret_data_news[time_tmp] += 1
    ret_data_news = one_hot2target(data2html(ret_data_news))
    # print(ret_data_news)

    # 方案6
    gkg_res = gkg.find({'gkgrecordid': {"$in": event_res_list}})
    ret_data_gkg = create_time_dict(start, end)
    res = gkg.find({'gkgrecordid': {"$in": event_res_list}})
    gkg_res_set = set()
    for item in res:
        time_tmp = item['date'][0:8]
        if time_tmp in ret_data_gkg:
            ret_data_gkg[time_tmp] += 1

    ret_data_gkg = one_hot2target(data2html(ret_data_gkg))
    # print(ret_data_gkg)

    ret_data = {'4': ret, '5': ret_data_news, '6': ret_data_gkg,'msg':msg}
    cnt=0
    for item in ret_data['4']['data']['data']:
        for num in item['data']:
            cnt+=num
    ret_data['4_all']=cnt
    ret_data['5_all']=calculate_all(ret_data['5'])
    ret_data['6_all']=calculate_all(ret_data['6'])
    print(ret_data)
    return ret_data

actor_all=['china']
actor_one=[]
actor_null=[]
#gkg_search_final(actor_all,actor_one,actor_null,"20181001","20181007",num=5000)