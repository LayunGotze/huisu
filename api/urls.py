from django.contrib import admin
from django.conf.urls import include, url
from api.views import *
urlpatterns=[
    url('news/',event_track_news),
    url('events/',event_track_event),
    url('gkg/',event_track_gkg)
]