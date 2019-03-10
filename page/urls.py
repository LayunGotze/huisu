from django.contrib import admin
from page.views import *
from django.conf.urls import include, url

urlpatterns=[
    url('test',test),
    url('get_demo',get_demo),
    url('event1', event1),
    url('event2', event2),
    url('event3', event3),
    url('event4', event4),
    url('event5', event5),
    url('event6', event6),
    url('event7', event7),
    url('event8', event8),
    url('event9', event9),
    url('news', news),
    url('event',event),
    url('gkg',gkg)
]