from django.shortcuts import render
import requests
import json
from django.http import JsonResponse
from api.backtrack_use.api_use import *
import json
from api.backtrack_use.event_basic_use import *
# Create your views here.

"""
9个方案的接口视图函数，接受前端发来的GET请求参数，返回JSON数据，前端直接展示
具体用到的函数可见api.backtrack_use.api_use
"""

event_map={'口头合作':[1,2,3,4,5],'实际合作':[6,7,8,9,10],'合作':[1,2,3,4,5,6,7,8,9,10],
           '口头冲突':[11,12,13,14,15],'实际冲突':[16,17,18,19,20],'冲突':[11,12,13,14,15,16,17,18,19,20],
           '全部':[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]}
def test(request):
    return JsonResponse({'res':"success"})

def event_track(request):
    #http://127.0.0.1:8000/api/event?actor1=[%27aaaa%27,%27bbb%27,%27cccc%27]
    actor1name=request.GET.getlist('actor1[]','')
    actor2name=request.GET.getlist('actor2[]','')
    eventcode = request.GET.getlist('code[]', -1)
    if len(actor1name)==1:
        actor1name=actor1name[0]
    if len(actor2name)==1:
        actor2name=actor2name[0]
    code=[]
    for item in eventcode:
        code.append(int(item))
    if len(code)==1:
        code=code[0]
    start = request.GET.get('start', '')
    end = request.GET.get('end', '')
    print(actor1name)
    print(actor2name)
    print(eventcode)
    print(start)
    print(end)
    ret=event_find(actor1name,actor2name,code,start,end)
    ret=dict2list(ret)
    return JsonResponse(ret)

def event_track_no1(request):
    #方案1，根据提供的人名输入和时间直接搜索新闻数据
    #返回热度图所需数据
    res={"time": ["20181001", "20181002", "20181003", "20181004", "20181005", "20181006", "20181007", "20181008", "20181009", "20181010", "20181011", "20181012", "20181013", "20181014", "20181015", "20181016", "20181017", "20181018", "20181019", "20181020", "20181021", "20181022", "20181023", "20181024", "20181025", "20181026", "20181027", "20181028", "20181029", "20181030", "20181031"], "legend": ["\u4e8b\u4ef6\u70ed\u5ea6"], "data": [{"name": ["\u4e8b\u4ef6\u70ed\u5ea6"], "type": "line", "smooth": "true", "data": [240, 263, 252, 247, 252, 290, 284, 137, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]}]}
    return JsonResponse(res)
    actor1 = request.GET.getlist('actor1[]', '')
    actor2 = request.GET.getlist('actor2[]', '')
    start = request.GET.get('start', '')
    end = request.GET.get('end', '')
    print(actor1)
    print(actor2)
    print(start)
    print(end)
    data=no1_news_only_search(actor1,actor2,start,end,num=2000)
    return JsonResponse(data)

def event_track_no2(request):
    #方案2，根据提供的人名输入和时间先搜索新闻数据，再联立事件数据库
    #返回热度图所需数据
    return JsonResponse(dict['2'])
    actor1 = request.GET.getlist('actor1[]', '')
    actor2 = request.GET.getlist('actor2[]', '')
    start = request.GET.get('start', '')
    end = request.GET.get('end', '')
    print(actor1)
    print(actor2)
    print(start)
    print(end)
    data=no2_news_only_search(actor1,actor2,start,end,num=2000)
    return JsonResponse(data)

def event_track_no3(request):
    #方案3，根据提供的输入和时间先搜索新闻数据，再联立GKG数据库
    #返回top个热门人物曲线所需数据
    return JsonResponse(dict['3'])
    actor1 = request.GET.getlist('actor1[]', '')
    actor2 = request.GET.getlist('actor2[]', '')
    start = request.GET.get('start', '')
    end = request.GET.get('end', '')
    print(actor1)
    print(actor2)
    print(start)
    print(end)
    data = no3_news_hot_search(actor1, actor2, start, end, num=2000)
    return JsonResponse(data)


def event_track_no4(request):
    #方案4，根据ACTOR,EVENT和时间搜索事件数据库，对各类事件热度进行回溯
    all=event_all_conclusion(dict['4']['data'])
    dict['4']['all']=all
    return JsonResponse(dict['4'])
    actor1 = request.GET.getlist('actor1[]', '')
    actor2 = request.GET.getlist('actor2[]', '')
    event=request.GET.get('event',[])
    start = request.GET.get('start', '口头合作')
    end = request.GET.get('end', '')
    event=event_map[event]
    print(actor1)
    print(actor2)
    print(event)
    print(start)
    print(end)
    data = no4_news_hot_all_search(actor1,actor2,event,start,end)
    return JsonResponse(data)


def event_track_no5(request):
    # 方案5，根据ACTOR,EVENT和时间搜索事件数据库，再找回新闻数据库统计热度
    all=event_all_conclusion(dict['5']['data'])
    dict['5']['all']=all
    return JsonResponse(dict['5'])
    actor1 = request.GET.getlist('actor1[]', '')
    actor2 = request.GET.getlist('actor2[]', '')
    event = request.GET.get('event', '口头合作')
    start = request.GET.get('start', '')
    end = request.GET.get('end', '')
    event = event_map[event]
    print(actor1)
    print(actor2)
    print(event)
    print(start)
    print(end)
    data = no5_news_hot_all_search(actor1, actor2, event, start, end)
    return JsonResponse(data)


def event_track_no6(request):
    # 方案6，根据ACTOR,EVENT和时间搜索事件数据库，再找回GKG统计国家热度
    all=event_all_conclusion(dict['6']['data'])
    dict['6']['all']=all
    return JsonResponse(dict['6'])
    actor1 = request.GET.getlist('actor1[]', '')
    actor2 = request.GET.getlist('actor2[]', '')
    event = request.GET.get('event', '口头合作')
    start = request.GET.get('start', '')
    end = request.GET.get('end', '')
    event = event_map[event]
    print(actor1)
    print(actor2)
    print(event)
    print(start)
    print(end)
    data = no6_news_hot_all_search(actor1, actor2, event, start, end)
    return JsonResponse(data)


def event_track_no7(request):
    # 方案7，根据ACTOR搜索GKG数据库，返回国家统计图
    return JsonResponse(dict['7'])
    actor1 = request.GET.getlist('actor1[]', '')
    actor2 = request.GET.getlist('actor2[]', '')
    start = request.GET.get('start', '')
    end = request.GET.get('end', '')
    print(actor1)
    print(actor2)
    print(start)
    print(end)
    data = no7_news_hot_search(actor1, actor2, start, end, num=2000)
    return JsonResponse(data)


def event_track_no8(request):
    # 方案8，根据ACTOR搜索GKG数据库，再查看英文新闻，返回时间热度图
    return JsonResponse(dict['8'])
    actor1 = request.GET.getlist('actor1[]', '')
    actor2 = request.GET.getlist('actor2[]', '')
    start = request.GET.get('start', '20181011')
    end = request.GET.get('end', '20181001')
    print(actor1)
    print(actor2)
    print(start)
    print(end)
    data = no8_news_only_search(actor1, actor2, start, end,num=2000)
    return JsonResponse(data)


def event_track_no9(request):
    # 方案9，根据ACTOR搜索GKG数据库，再查看事件数据库，返回10个最热人物
    return JsonResponse(dict['9'])
    actor1 = request.GET.getlist('actor1[]', '')
    actor2 = request.GET.getlist('actor2[]', '')
    start = request.GET.get('start', '20181011')
    end = request.GET.get('end', '20181001')
    print(actor1)
    print(actor2)
    print(start)
    print(end)
    data = no9_news_hot_search(actor1, actor2, start, end,num=2000)
    return JsonResponse(data)

def event_track_news(request):
    #方案1，2，3，返回1，2，3的数据
    actor1 = request.GET.getlist('actor1[]', '')
    actor2 = request.GET.getlist('actor2[]', '')
    start = request.GET.get('start', '20181011')
    end = request.GET.get('end', '20181001')
    print(actor1)
    print(actor2)
    print(start)
    print(end)
    data=news_search(actor1,actor2,start,end,num=2000)
    return JsonResponse(data)

def event_track_event(request):
    #方案4，5，6
    actor1 = request.GET.getlist('actor1[]', '')
    actor2 = request.GET.getlist('actor2[]', '')
    event = request.GET.get('event', '口头合作')
    start = request.GET.get('start', '')
    end = request.GET.get('end', '')
    event = event_map[event]
    print(actor1)
    print(actor2)
    print(event)
    print(start)
    print(end)
    data=event_search(actor1,actor2,event,start,end)
    return JsonResponse(data)

def event_track_gkg(request):
    # 方案7,8,9
    actor1 = request.GET.getlist('actor1[]', '')
    actor2 = request.GET.getlist('actor2[]', '')
    start = request.GET.get('start', '20181011')
    end = request.GET.get('end', '20181001')
    print(actor1)
    print(actor2)
    print(start)
    print(end)
    data=gkg_search(actor1,actor2,start,end)
    return JsonResponse(data)
