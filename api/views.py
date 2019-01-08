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

event_map={'口头合作':[1],'实际合作':[2],'合作':[1,2],'口头冲突':[3],'实际冲突':[4],'冲突':[3,4],'全部':[1,2,3,4]}
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
    return JsonResponse(dict['1'])
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
    data = no3_news_only_search(actor1, actor2, start, end,num=2000,top=11)
    return JsonResponse(data)


def event_track_no4(request):
    #方案4，根据ACTOR,EVENT和时间搜索事件数据库，对各类事件热度进行回溯
    res={'口头合作': {'hot': [[1522512000000, 5], [1522598400000, 24], [1522684800000, 18], [1522771200000, 17], [1522857600000, 17], [1522944000000, 11], [1523376000000, 3], [1523462400000, 1], [1524067200000, 8], [1524153600000, 13], [1524240000000, 5], [1524326400000, 18], [1524412800000, 23], [1524499200000, 21], [1524585600000, 20], [1524672000000, 22], [1524758400000, 18], [1524844800000, 6], [1524931200000, 7], [1525017600000, 11]], 'max_value': 24, 'min_value': 0}, '实际合作': {'hot': [[1522512000000, 16], [1522598400000, 12], [1522684800000, 8], [1522771200000, 15], [1522857600000, 15], [1522944000000, 3], [1523289600000, 3], [1524067200000, 2], [1524153600000, 5], [1524240000000, 2], [1524326400000, 6], [1524412800000, 1], [1524585600000, 4], [1524672000000, 5], [1524758400000, 2], [1524931200000, 3], [1525017600000, 9]], 'max_value': 16, 'min_value': 0}, '口头冲突': {'hot': [[1522512000000, 8], [1522598400000, 36], [1522684800000, 24], [1522771200000, 31], [1522857600000, 19], [1522944000000, 28], [1523203200000, 1], [1523289600000, 1], [1524067200000, 8], [1524153600000, 3], [1524240000000, 4], [1524326400000, 4], [1524412800000, 11], [1524499200000, 7], [1524585600000, 13], [1524672000000, 9], [1524758400000, 13], [1525017600000, 3]], 'max_value': 36, 'min_value': 0}, '实际冲突': {'hot': [], 'max_value': -1, 'min_value': 0}}
    return JsonResponse(res)
    actor1 = request.GET.getlist('actor1[]', '')
    actor2 = request.GET.getlist('actor2[]', '')
    event=request.GET.get('event','口头合作')
    start = request.GET.get('start', '')
    end = request.GET.get('end', '')
    event=event_map[event]
    print(actor1)
    print(actor2)
    print(event)
    print(start)
    print(end)
    data = no4_news_only_search(actor1,actor2,event,start,end)
    return JsonResponse(data)


def event_track_no5(request):
    # 方案5，根据ACTOR,EVENT和时间搜索事件数据库，再找回新闻数据库统计热度
    res={'hot': [[1522512000000, 15], [1522598400000, 50], [1522684800000, 56], [1522771200000, 43], [1522857600000, 54], [1522944000000, 55], [1523030400000, 0], [1523116800000, 0], [1523203200000, 0], [1523289600000, 0], [1523376000000, 0], [1523462400000, 0], [1523548800000, 0], [1523635200000, 0], [1523721600000, 0], [1523808000000, 0], [1523894400000, 0], [1523980800000, 0], [1524067200000, 9], [1524153600000, 24], [1524240000000, 13], [1524326400000, 14], [1524412800000, 35], [1524499200000, 30], [1524585600000, 37], [1524672000000, 33], [1524758400000, 27], [1524844800000, 20], [1524931200000, 8], [1525017600000, 14]], 'max_value': 56, 'min_value': 0}
    return JsonResponse(res)
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
    data = no5_news_only_search(actor1, actor2, event, start, end)
    return JsonResponse(data)


def event_track_no6(request):
    # 方案6，根据ACTOR,EVENT和时间搜索事件数据库，再找回GKG统计国家热度
    res={'country': ['美国', '中国', '印尼', '朝鲜 北朝鲜', '韩国', '越南', '日本', '印度', '俄罗斯', '菲律宾'], 'hot': [6005, 2736, 1023, 264, 179, 160, 97, 93, 88, 87]}
    return JsonResponse(res)
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
    data = no6_news_only_search(actor1, actor2, event, start, end,10)
    return JsonResponse(data)


def event_track_no7(request):
    # 方案7，根据ACTOR搜索GKG数据库，返回国家统计图
    res={'name': ['美国', '印尼', '俄罗斯', '伊朗', '以色列', '韩国', '德国', '朝鲜 北朝鲜', '圣文森特和格林纳丁斯', '英国', '中国', '肯尼亚', '洪都拉斯', '法国', '日本', '中国香港'], 'hot': [144, 51, 25, 23, 15, 11, 11, 9, 8, 7, 7, 5, 5, 3, 3, 3]}
    return JsonResponse(dict['7'])
    actor1 = request.GET.getlist('actor1[]', '')
    actor2 = request.GET.getlist('actor2[]', '')
    start = request.GET.get('start', '')
    end = request.GET.get('end', '')
    print(actor1)
    print(actor2)
    print(start)
    print(end)
    data = no7_news_only_search(actor1, actor2, start, end)
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
    data = no8_news_only_search(actor1, actor2, start, end)
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
    data = no9_news_only_search(actor1, actor2, start, end)
    return JsonResponse(data)
