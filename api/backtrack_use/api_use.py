import time
import re
from api.backtrack_use.mongodb_link import origin,events_tracking

def timestr2stamp13(timestr):
    #将形如"20180506"的时间字符串转换成13位时间戳整数，便于前端展示
    return int(time.mktime(time.strptime(timestr,'%Y%m%d'))*1000)

def senid2index(sentid):
    #将形如"592436239afc10f2c9a240c8_12"的SENTID分解为ID和INDE，其中，INDEX转换为整数
    res=sentid.split('_')
    id=res[0]
    index=int(res[1])
    return id,index

def find_origin(sentid):
    #根据ID和INDEX查询ORIGIN库中的文章信息
    res = sentid.split('_')
    id = res[0]
    index = int(res[1])
    item=origin.find({'story_id':id})
    if item.count()==0:
        return {"msg":"no result"}
    item=item[0]
    ret={"msg":"success"}
    ret['res']={}
    ret['res']['title']=item['s_title']
    ret['res']['url']=item['o_url']
    ret['res']['sent']=item['s_parsed']['unparsed_sents'][int(index)].strip()
    return ret
#id,index=senid2index('5ae994a9aacf802249155fb3_0')
#print(find_origin(id,index)

def event_combine_by_name(actor1name='',actor2name='',eventcode=-1,begindate='',enddate=''):
    #根据ACTOR1和ACTOR2查找时间回溯信息，包括时间和地点,不包括经纬度，完全版
    #必须提供前3个参数，否则要返回错误信息，后面两个时间参数可不写
    #event_combine_by_name('President','China',55,'20180501','20180506')
    #删除没有完全地理信息名称的项
    if eventcode==-1:
        return {"msg":"没有提供事件名称"}
    if actor1name=='' or actor2name=='':
        return {"msg":"需提供参与事件人的姓名"}
    bool_actor1=0
    bool_actor2=0#表示ACTOR1 2 NAME是否在字典中的布尔变量
    if actor1name in name2code_dict:
        bool_actor1=1
    if actor2name in name2code_dict:
        bool_actor2=1
    if bool_actor1==0 and bool_actor2==0:
        #两个姓名都未出现过
        return {'msg':'无搜索结果'}
    actor1code=[]
    actor2code=[]
    search_dict = {}
    if begindate!='' and enddate!='':
        search_dict['sqldate']={'$gte':begindate,'$lte':enddate}
    elif begindate!='' and enddate=='':
        search_dict['sqldate'] = {'$gte': begindate}
    elif begindate=='' and enddate!='':
        search_dict['sqldate'] = {'$lte': enddate}
    #排除缺少地理信息的
    search_dict['actor1geo_fullname'] = {"$not": {"$in": ['']}}
    search_dict['actor2geo_fullname'] = {"$not": {"$in": ['']}}
    if type(eventcode)==list:
        search_dict['eventcode'] = {"$in":eventcode}
    elif eventcode==-1:
        return {"msg":"没有此事件"}
    else:
        search_dict['eventcode'] = eventcode
    if bool_actor1==1 and bool_actor2==1:
        #两个姓名都出现了
        actor1code = name2code_dict[actor1name]
        actor2code = name2code_dict[actor2name]
        #search_dict['actor1code']={"$in":actor1code}
        #search_dict['actor2code']={"$in":actor2code}
        search_dict['actor1name']=actor1name
        search_dict['actor2name']=actor2name
    if bool_actor1==1 and bool_actor2==0:
        #出现了1没有2
        actor1code = name2code_dict[actor1name]
        search_dict['actor2code'] = {"$in": actor1code}
        search_dict['actor1name'] = actor1name
    if bool_actor1==0 and bool_actor2==1:
        #出现了2没有1
        actor2code = name2code_dict[actor2name]
        search_dict['actor1code'] = {"$in": actor2code}
        search_dict['actor2name'] = actor2name
    #以上都是生成查询语句
    print(search_dict)
    res=events_tracking.find(search_dict)
    if(res.count()==0):
        return {"total":0,"msg":'无结果'}
    """
    want_key=['sqldate','sentid','actor1geo_long', 'actiongeo_fullname', 'actor1geo_adm1code',
              'actiongeo_lat', 'actor2geo_countrycode', 'actor2geo_type', 'actor1geo_lat',
              'actor1geo_fullname', 'actor2geo_long', 'actor2geo_lat', 'actor1geo_type',
              'actiongeo_adm1code', 'actiongeo_featureid', 'actor1geo_countrycode', 'actiongeo_long',
              'actor1geo_featureid', 'actor2geo_featureid', 'actor2geo_adm1code', 'actiongeo_type',
              'actor2geo_fullname', 'actiongeo_countrycode']
    """
    want_key=['sqldate','sentid','actor2geo_fullname','actor1geo_fullname','eventcode','eventverb']

    ret={}
    ret['total']=res.count()
    res_list=[]
    for item in res:
        tmp_dict={}
        for key in want_key:
            if key in item:
                tmp_dict[key]=item[key]
            else:
                tmp_dict[key]="null"
        """
        for key in geo_key:
            if tmp_dict[key]!="null":
                tmp_dict['lat'],tmp_dict['log']=geo2lat(tmp_dict[key])
        """
        res_list.append(tmp_dict)
    ret['res']=res_list
    ret['msg']='success'
    ret['actor1name']=actor1name
    ret['actor2name']=actor2name
    return ret

def all_geo2lat(dict):
    #接受event_combine_by_name的全部返回值，将里面的地址名称加入经纬度信息
    #在原基础上将GEOFULLNAME改为 {"name":"asdas","lat":123,"log":123}的形式
    if 'res' not in dict:
        return {'msg':'no result'}
    list=dict['res']
    print(list)
    actor1name=dict['actor1name']
    actor2name=dict['actor2name']
    geo_key=['actor1geo_fullname','actor2geo_fullname']
    map={}
    for item in list:
        for key in geo_key:
            tmp = {}
            tmp['origin'] = find_origin(item['sentid'])
            tmp['time'] = item['sqldate']
            geo=item[key]
            if geo!="null":
                if geo not in map:
                    tmp['lat'],tmp['lon']=geo2lat(item[key])
                    map[geo]={'lat':tmp['lat'],'lon':tmp['lon']}
                elif geo in map:
                    tmp['lat']=map[geo]['lat']
                    tmp['lon']=map[geo]['lon']
                if key=='actor1geo_fullname':
                    tmp['color']='red'
                    tmp['name']=actor1name
                    tmp['geo'] = geo
                elif key=='actor2geo_fullname':
                    tmp['color']='blue'
                    tmp['name']=actor2name
                    tmp['geo'] = geo
                    #if item['actor1geo_fullname']!="null":
                    tmp['hub'] = item['actor1geo_fullname']
                key=key+'1'
                item[key]=tmp
    return dict

def event_find(actor1name='',actor2name='',eventcode=-1,begindate='',enddate=''):
    #根据提供的信息进行回溯，返回每个时间的事件个数与情感总值
    #event_combine_by_name('President','China',55,'20180501','20180506')
    #其中前三个参数可以是list
    if eventcode == -1:
        return {"msg": "没有提供事件名称"}
    if actor1name == '' or actor2name == '':
        return {"msg": "需提供参与事件人的姓名"}
    search_dict = {}

    #时间范围
    if begindate != '' and enddate != '':
        search_dict['sqldate'] = {'$gte': begindate, '$lte': enddate}
    elif begindate != '' and enddate == '':
        search_dict['sqldate'] = {'$gte': begindate}
    elif begindate == '' and enddate != '':
        search_dict['sqldate'] = {'$lte': enddate}

    #eventcode搜索
    if type(eventcode) == list:
        search_dict['eventcode'] = {"$in": eventcode}
    elif eventcode == -1:
        return {"msg": "没有此事件"}
    else:
        search_dict['eventcode'] = eventcode

    #actorname搜索
    if type(actor1name)==list:
        search_dict['actor1name'] = {"$in":actor1name}
    else:
        search_dict['actor1name']=actor1name
    if type(actor2name)==list:
        search_dict['actor2name']={"$in":actor2name}
    else:
        search_dict['actor2name'] = actor2name
    print(search_dict)

    res=events_tracking.find(search_dict)
    if (res.count() == 0):
        return {"total": 0, "msg": '无结果'}
    ret={}
    ret['total']=res.count()
    ret['msg']="success"
    for item in res:
        print(item['sqldate'])
        if item['sqldate'] not in ret:
            ret[item['sqldate']]={'num':1,'sentiment':0}
            if item['avgtone']!='':
                ret[item['sqldate']]['sentiment']=ret[item['sqldate']]['sentiment']+item['avgtone']
        else:
            ret[item['sqldate']]['num']=ret[item['sqldate']]['num']+1
            if item['avgtone']!='':
                ret[item['sqldate']]['sentiment']=ret[item['sqldate']]['sentiment']+item['avgtone']
    print(ret)
    return ret

#print(event_find(['President','Japan'],'China',[55,100,40,10],'20180501','20180706'))
def dict2list(res_dict):
    #将查询所得的dict转换成便于前端曲线表展示的list
    #接受event_find返回的字典结果
    ret={'sentiment':[],'hot':[],'senti_max':-10,'senti_min':10,'hot_max':-1,'hot_min':10}
    if res_dict['msg']!='success':
        return ret
    res_dict.pop('total')
    res_dict.pop('msg')
    for key in res_dict:
        timestamp=timestr2stamp13(key)
        tmp_sentiment=res_dict[key]['sentiment']
        tmp_hot=res_dict[key]['num']
        ret['sentiment'].append([timestamp,tmp_sentiment])
        ret['hot'].append([timestamp,tmp_hot])
        ret['senti_max']=max(ret['senti_max'],tmp_sentiment)
        ret['senti_min']=min(ret['senti_min'],tmp_sentiment)
        ret['hot_max']=max(ret['hot_max'],tmp_hot)
        ret['hot_min']=min(ret['hot_min'],tmp_hot)
    ret['senti_max']=ret['senti_max']+1
    ret['senti_min']=ret['senti_min']-1
    ret['hot_max']=ret['hot_max']+1
    ret['hot_min']=ret['hot_min']-1
    ret['sentiment'].sort()
    ret['hot'].sort()
    return ret

#event_find(['President', 'Japan'],'China',['55', '100', '40', '10', '20', '11', '16'],'20180101','20181030')
#print(event_find(['President','Japan'],'China',[55,100,40,10],'20180501','20180706'))
def timestr2stamp10(time_str):
    #将'20180501'的字符串转换为10位时间戳
    return int(time.mktime(time.strptime(time_str, "%Y%m%d")))

def gkg_person_list(data):
    #将gkg中的person字符串转换成list
    list=[]
    if(data==""):
        return list
    list=data.split(';')
    return list

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

def dict_sort(dict,num):
    #将dict按值排序，返回前num位的二维数组，每个数字包含key,value
    items=dict.items()
    backitem=[[v[1],v[0]] for v in items]
    backitem.sort(reverse=True)
    backitem=backitem[:10]
    for item in backitem:
        item.reverse()
    return backitem


def no1_news_only_search(actor1,actor2,start,end):
    #方案一，直接查询英文新闻，返回热度图
    #actor1,actor2为长度相等的数组，相同索引位置表示一组
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
    res=origin.find(dict).limit(10000)
    #print(res.count())
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
                        cnt+=1
            except:
                continue
        except StopIteration:
            print('finished')
            break
        except Exception as e:
            print(e)
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


#以下为no1_news_only_search和data2html的测试函数
#data={'20180501': 607, '20180502': 0, '20180503': 0, '20180504': 0, '20180505': 0, '20180506': 0}
#print(data2html(data))
#data=no2_news_only_search(actor1,actor2,"20180506","20180515")
#print(data2html(data))
#print(time.strftime("%Y%m%d",time.localtime(1495545426)))
#print(data)



#data=no3_news_only_search(actor1,actor2,"20180506","20180515")
#print(data)

#data=no4_news_only_search(actor1,actor2,event,"20180401","20181030")
#print(data)
