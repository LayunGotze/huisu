from django.shortcuts import render
import requests
import json
from django.http import JsonResponse
from api.backtrack_use.api_use import *
# Create your views here.
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
    actor1 = request.GET.getlist('actor1[]', '')
    actor2 = request.GET.getlist('actor2[]', '')
    start = request.GET.get('start', '')
    end = request.GET.get('end', '')
    print(actor1)
    print(actor2)
    print(start)
    print(end)
    #data=no1_news_only_search(actor1,actor2,start,end)
    data={'20180501': 607, '20180502': 0, '20180503': 0, '20180504': 0, '20180505': 0, '20180506': 0}
    data=data2html(data)
    return JsonResponse(data)