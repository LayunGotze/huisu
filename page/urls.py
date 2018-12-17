from django.contrib import admin
from page.views import *
from django.conf.urls import include, url

urlpatterns=[
    url('test',test),
    url('get_demo',get_demo),
    url('event1',event1)
]