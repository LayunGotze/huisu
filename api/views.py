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
    #return JsonResponse(dict['1'])
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
    #return JsonResponse(dict['2'])
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
    #return JsonResponse(dict['3'])
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
    res={'data':{'time': ['20180402', '20180403', '20180404', '20180405', '20180406', '20180407', '20180408', '20180409', '20180410'], 'legend': ['口头合作', '实际合作', '口头冲突', '实际冲突'], 'data': [{'name': '口头合作', 'type': 'line', 'smooth': 'true', 'data': [27, 84, 97, 109, 68, 68, 0, 0, 1]}, {'name': '实际合作', 'type': 'line', 'smooth': 'true', 'data': [5, 11, 23, 31, 23, 13, 0, 0, 0]}, {'name': '口头冲突', 'type': 'line', 'smooth': 'true', 'data': [3, 4, 19, 10, 12, 6, 0, 1, 0]}, {'name': '实际冲突', 'type': 'line', 'smooth': 'true', 'data': [4, 6, 20, 20, 21, 33, 0, 0, 0]}]},
    'all':{1: {'time': ['20180401', '20180402', '20180403', '20180404', '20180405', '20180406', '20180407', '20180408', '20180409', '20180410'], 'legend': ['事件热度'], 'data': [{'name': ['事件热度'], 'type': 'line', 'smooth': 'true', 'data': [2, 34, 38, 51, 21, 12, 0, 0, 0, 1]}]},
    2: {'time': ['20180401', '20180402', '20180403', '20180404', '20180405', '20180406', '20180407', '20180408', '20180409', '20180410'], 'legend': ['事件热度'], 'data': [{'name': ['事件热度'], 'type': 'line', 'smooth': 'true', 'data': [0, 1, 3, 10, 5, 12, 0, 0, 0, 0]}]},
    3: {'time': ['20180401', '20180402', '20180403', '20180404', '20180405', '20180406', '20180407', '20180408', '20180409', '20180410'], 'legend': ['事件热度'], 'data': [{'name': ['事件热度'], 'type': 'line', 'smooth': 'true', 'data': [5, 27, 30, 23, 20, 25, 0, 0, 0, 0]}]},
    4: {'time': ['20180401', '20180402', '20180403', '20180404', '20180405', '20180406', '20180407', '20180408', '20180409', '20180410'], 'legend': ['事件热度'], 'data': [{'name': ['事件热度'], 'type': 'line', 'smooth': 'true', 'data': [19, 19, 24, 17, 15, 16, 0, 0, 1, 0]}]},
    5: {'time': ['20180401', '20180402', '20180403', '20180404', '20180405', '20180406', '20180407', '20180408', '20180409', '20180410'], 'legend': ['事件热度'], 'data': [{'name': ['事件热度'], 'type': 'line', 'smooth': 'true', 'data': [1, 3, 2, 8, 7, 3, 0, 0, 0, 0]}]},
    6: {'time': ['20180401', '20180402', '20180403', '20180404', '20180405', '20180406', '20180407', '20180408', '20180409', '20180410'], 'legend': ['事件热度'], 'data': [{'name': ['事件热度'], 'type': 'line', 'smooth': 'true', 'data': [1, 4, 13, 16, 18, 6, 0, 0, 0, 0]}]},
    7: {'time': ['20180401', '20180402', '20180403', '20180404', '20180405', '20180406', '20180407', '20180408', '20180409', '20180410'], 'legend': ['事件热度'], 'data': [{'name': ['事件热度'], 'type': 'line', 'smooth': 'true', 'data': [0, 0, 1, 3, 3, 1, 0, 0, 0, 0]}]},
    8: {'time': ['20180401', '20180402', '20180403', '20180404', '20180405', '20180406', '20180407', '20180408', '20180409', '20180410'], 'legend': ['事件热度'], 'data': [{'name': ['事件热度'], 'type': 'line', 'smooth': 'true', 'data': [4, 2, 7, 5, 1, 0, 0, 0, 0, 0]}]},
    9: {'time': ['20180401', '20180402', '20180403', '20180404', '20180405', '20180406', '20180407', '20180408', '20180409', '20180410'], 'legend': ['事件热度'], 'data': [{'name': ['事件热度'], 'type': 'line', 'smooth': 'true', 'data': [0, 4, 2, 6, 0, 1, 0, 0, 0, 4]}]},
    10: {'time': ['20180401', '20180402', '20180403', '20180404', '20180405', '20180406', '20180407', '20180408', '20180409', '20180410'], 'legend': ['事件热度'], 'data': [{'name': ['事件热度'], 'type': 'line', 'smooth': 'true', 'data': [0, 1, 0, 1, 1, 5, 0, 0, 0, 0]}]},
    11: {'time': ['20180401', '20180402', '20180403', '20180404', '20180405', '20180406', '20180407', '20180408', '20180409', '20180410'], 'legend': ['事件热度'], 'data': [{'name': ['事件热度'], 'type': 'line', 'smooth': 'true', 'data': [2, 3, 9, 5, 9, 3, 0, 1, 0, 0]}]},
    12: {'time': ['20180401', '20180402', '20180403', '20180404', '20180405', '20180406', '20180407', '20180408', '20180409', '20180410'], 'legend': ['事件热度'], 'data': [{'name': ['事件热度'], 'type': 'line', 'smooth': 'true', 'data': [1, 1, 4, 4, 0, 0, 0, 0, 0, 0]}]},
    13: {'time': ['20180401', '20180402', '20180403', '20180404', '20180405', '20180406', '20180407', '20180408', '20180409', '20180410'], 'legend': ['事件热度'], 'data': [{'name': ['事件热度'], 'type': 'line', 'smooth': 'true', 'data': [0, 0, 2, 0, 3, 3, 0, 0, 0, 0]}]},
    14: {'time': ['20180401', '20180402', '20180403', '20180404', '20180405', '20180406', '20180407', '20180408', '20180409', '20180410'], 'legend': ['事件热度'], 'data': [{'name': ['事件热度'], 'type': 'line', 'smooth': 'true', 'data': [0, 0, 3, 1, 0, 0, 0, 0, 0, 0]}]},
    15: {'time': ['20180401', '20180402', '20180403', '20180404', '20180405', '20180406', '20180407', '20180408', '20180409', '20180410'], 'legend': ['事件热度'], 'data': [{'name': ['事件热度'], 'type': 'line', 'smooth': 'true', 'data': [0, 0, 1, 0, 0, 0, 0, 0, 0, 0]}]},
    16: {'time': ['20180401', '20180402', '20180403', '20180404', '20180405', '20180406', '20180407', '20180408', '20180409', '20180410'], 'legend': ['事件热度'], 'data': [{'name': ['事件热度'], 'type': 'line', 'smooth': 'true', 'data': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]}]},
    17: {'time': ['20180401', '20180402', '20180403', '20180404', '20180405', '20180406', '20180407', '20180408', '20180409', '20180410'], 'legend': ['事件热度'], 'data': [{'name': ['事件热度'], 'type': 'line', 'smooth': 'true', 'data': [2, 4, 13, 15, 15, 31, 0, 0, 0, 0]}]},
    18: {'time': ['20180401', '20180402', '20180403', '20180404', '20180405', '20180406', '20180407', '20180408', '20180409', '20180410'], 'legend': ['事件热度'], 'data': [{'name': ['事件热度'], 'type': 'line', 'smooth': 'true', 'data': [0, 1, 0, 0, 0, 1, 0, 0, 0, 0]}]},
    19: {'time': ['20180401', '20180402', '20180403', '20180404', '20180405', '20180406', '20180407', '20180408', '20180409', '20180410'], 'legend': ['事件热度'], 'data': [{'name': ['事件热度'], 'type': 'line', 'smooth': 'true', 'data': [2, 1, 7, 5, 6, 1, 0, 0, 0, 0]}]},
    20: {'time': ['20180401', '20180402', '20180403', '20180404', '20180405', '20180406', '20180407', '20180408', '20180409', '20180410'], 'legend': ['事件热度'], 'data': [{'name': ['事件热度'], 'type': 'line', 'smooth': 'true', 'data': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]}]}}}
    #return JsonResponse(res)
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
    res={'data':{
        'time': ['20180401', '20180402', '20180403', '20180404', '20180405', '20180406', '20180407', '20180408', '20180409', '20180410'],
        'legend': ['口头合作', '实际合作', '口头冲突', '实际冲突'], 'data': [
            { 'name': '口头合作', 'type': 'line', 'smooth': 'true', 'data': [33, 33, 54, 27, 41, 44, 0, 0, 0, 0] },
            { 'name': '实际合作', 'type': 'line', 'smooth': 'true', 'data': [53, 65, 137, 79, 151, 96, 0, 0, 0, 0] },
            { 'name': '口头冲突', 'type': 'line', 'smooth': 'true', 'data': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0] },
            { 'name': '实际冲突', 'type': 'line', 'smooth': 'true', 'data': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0] }]
    },
    'all':{
        4: { 'time': ['20180401', '20180402', '20180403', '20180404', '20180405', '20180406', '20180407', '20180408', '20180409', '20180410'], 'legend': ['事件热度'], 'data': [{ 'name': ['事件热度'], 'type': 'line', 'smooth': 'true', 'data': [16, 15, 26, 11, 17, 20, 0, 0, 0, 0] }] },
        5: { 'time': ['20180401', '20180402', '20180403', '20180404', '20180405', '20180406', '20180407', '20180408', '20180409', '20180410'], 'legend': ['事件热度'], 'data': [{ 'name': ['事件热度'], 'type': 'line', 'smooth': 'true', 'data': [17, 18, 28, 16, 24, 24, 0, 0, 0, 0] }] },
        6: { 'time': ['20180401', '20180402', '20180403', '20180404', '20180405', '20180406', '20180407', '20180408', '20180409', '20180410'], 'legend': ['事件热度'], 'data': [{ 'name': ['事件热度'], 'type': 'line', 'smooth': 'true', 'data': [17, 21, 43, 24, 47, 31, 0, 0, 0, 0] }] },
        7: { 'time': ['20180401', '20180402', '20180403', '20180404', '20180405', '20180406', '20180407', '20180408', '20180409', '20180410'], 'legend': ['事件热度'], 'data': [{ 'name': ['事件热度'], 'type': 'line', 'smooth': 'true', 'data': [17, 21, 43, 25, 52, 32, 0, 0, 0, 0] }] },
        8: { 'time': ['20180401', '20180402', '20180403', '20180404', '20180405', '20180406', '20180407', '20180408', '20180409', '20180410'], 'legend': ['事件热度'], 'data': [{ 'name': ['事件热度'], 'type': 'line', 'smooth': 'true', 'data': [19, 23, 51, 30, 52, 33, 0, 0, 0, 0] }] }
    }}

    #return JsonResponse(res)
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
    res={'data':{
        'time': ['20180401', '20180402', '20180403', '20180404', '20180405', '20180406', '20180407', '20180408', '20180409', '20180410'], 'legend': ['口头合作', '实际合作', '口头冲突', '实际冲突'],
        'data': [{ 'name': '口头合作', 'type': 'line', 'smooth': 'true', 'data': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0] },
        { 'name': '实际合作', 'type': 'line', 'smooth': 'true', 'data': [0, 7, 6, 11, 3, 7, 0, 0, 0, 0] },
        { 'name': '口头冲突', 'type': 'line', 'smooth': 'true', 'data': [3, 14, 21, 29, 26, 20, 0, 0, 0, 0] },
        { 'name': '实际冲突', 'type': 'line', 'smooth': 'true', 'data': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0] }]
    },
        'all':{9: {'time': ['20180401', '20180402', '20180403', '20180404', '20180405', '20180406', '20180407', '20180408', '20180409', '20180410'], 'legend': ['事件热度'], 'data': [{'name': ['事件热度'], 'type': 'line', 'smooth': 'true', 'data': [0, 3, 3, 5, 1, 1, 0, 0, 0, 0]}]},
        10: {'time': ['20180401', '20180402', '20180403', '20180404', '20180405', '20180406', '20180407', '20180408', '20180409', '20180410'], 'legend': ['事件热度'], 'data': [{'name': ['事件热度'], 'type': 'line', 'smooth': 'true', 'data': [0, 4, 3, 6, 2, 6, 0, 0, 0, 0]}]},
        11: {'time': ['20180401', '20180402', '20180403', '20180404', '20180405', '20180406', '20180407', '20180408', '20180409', '20180410'], 'legend': ['事件热度'], 'data': [{'name': ['事件热度'], 'type': 'line', 'smooth': 'true', 'data': [1, 7, 10, 11, 13, 10, 0, 0, 0, 0]}]},
        12: {'time': ['20180401', '20180402', '20180403', '20180404', '20180405', '20180406', '20180407', '20180408', '20180409', '20180410'], 'legend': ['事件热度'], 'data': [{'name': ['事件热度'], 'type': 'line', 'smooth': 'true', 'data': [2, 7, 11, 18, 13, 10, 0, 0, 0, 0]}]}}
    }

    #return JsonResponse(res)
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
