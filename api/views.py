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

event_map={21:[1,2,3,4,5],22:[6,7,8,9,10],
           23:[11,12,13,14,15],24:[16,17,18,19,20],
           25:[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20],
           0:[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]}

def event_track_news(request):
    #方案1，2，3，返回1，2，3的数据
    actor1 = request.GET.getlist('actor1[]', '')
    actor2 = request.GET.getlist('actor2[]', '')
    start = request.GET.get('start', '20181001')
    end = request.GET.get('end', '20181001')
    print(actor1)
    print(actor2)
    print(start)
    print(end)
    data=news_search(actor1,actor2,start,end,num=2000)
    return JsonResponse(data)

def event_track_event(request):
    #方案4，5，6

    event = request.GET.get('event', 0)
    start = request.GET.get('start', '')
    end = request.GET.get('end', '')
    actor1country = request.GET.get('actor1country', '')
    actor1code = request.GET.get('actor1code', '')
    actor2country = request.GET.get('actor2country', '')
    actor2code = request.GET.get('actor2code', '')
    location=request.GET.get('location','')
    event=int(event)
    event_list=[]
    if event>=1 and event<=20:
        event_list.append(event)
    else:
        event_list=event_map[event]
    print(actor1country,actor1code)
    print(actor1country,actor1code)
    print(location)
    print(event_list)
    print(start)
    print(end)
    data=event_search_final(actor1country,actor1code,actor1country,actor1code,event_list,location,start,end)
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
