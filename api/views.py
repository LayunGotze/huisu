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
    actor1name=request.GET.get('actor1','')
    actor2name=request.GET.get('actor2','')
    eventcode = request.GET.get('code', -1)
    start = request.GET.get('start', '')
    end = request.GET.get('end', '')
    print(actor1name)
    print(type(actor1name))
    actor1name=list(actor1name)
    print(type(actor1name))
    ret=event_find(actor1name,actor2name,eventcode,start,end)
    ret=dict2list(ret)
    return JsonResponse(ret)