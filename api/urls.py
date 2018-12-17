from django.contrib import admin
from django.conf.urls import include, url
from api.views import *
urlpatterns=[
    url('test/',test),
    url('event/',event_track),
    url('event1/',event_track_no1)
]