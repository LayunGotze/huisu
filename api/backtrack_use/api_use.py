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

def no1_news_only_search(start,end):
    #方案一，直接查询英文新闻，返回热度图
    dict={"o_gt":{"$gte":timestr2stamp10(start),"$lte":timestr2stamp10(end)}}
    print(dict)
    cnt=0
    res=origin.find(dict)
    res=res[0:250]

    for item in res:
        try:
            if 's_cont' in item:
                res1=re.search("China",item['s_cont'])
                res2=re.search("USA",item['s_cont'])
                if res1 is not None and res2 is not None:
                    cnt=cnt+1
                    print(cnt)
        except Exception as e:
            print(e)
            continue
no1_news_only_search("20180501","20180503")