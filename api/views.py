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
    actor_all = request.GET.get('actor_all', '')
    actor_one = request.GET.get('actor_one', '')
    actor_null = request.GET.get('actor_null', '')
    start = request.GET.get('start', '20181001')
    end = request.GET.get('end', '20181001')

    actor_all = str(actor_all)
    actor_one = str(actor_one)
    actor_null = str(actor_null)

    actor_all = [] if actor_all == "" else actor_all.split(';')
    actor_one = [] if actor_one == "" else actor_one.split(';')
    actor_null = [] if actor_null == "" else actor_null.split(';')

    print(actor_all)
    print(actor_one)
    print(actor_null)
    print(start)
    print(end)
    data=news_search_final(actor_all,actor_one,actor_null,start,end,num=0)
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
    actor_all = request.GET.get('actor_all', '')
    actor_one = request.GET.get('actor_one', '')
    actor_null = request.GET.get('actor_null', '')
    start = request.GET.get('start', '20181001')
    end = request.GET.get('end', '20181001')

    actor_all=str(actor_all)
    actor_one=str(actor_one)
    actor_null=str(actor_null)

    actor_all = [] if actor_all=="" else actor_all.split(';')
    actor_one = [] if actor_one=="" else actor_one.split(';')
    actor_null =[] if actor_null=="" else actor_null.split(';')

    print(actor_all)
    print(actor_one)
    print(actor_null)
    print(start)
    print(end)

    data=gkg_search_final(actor_all,actor_one,actor_null,start,end,num=0)
    return JsonResponse(data)
