from django.contrib import admin
from django.conf.urls import include, url
from api.views import *
urlpatterns=[
    url('test/',test),
    url('event/',event_track),
    url('event1/', event_track_no1),
    url('event2/', event_track_no2),
    url('event3/', event_track_no3),
    url('event4/', event_track_no4),
    url('event5/', event_track_no5),
    url('event6/', event_track_no6),
    url('event7/', event_track_no7),
    url('event8/', event_track_no8),
    url('event9/', event_track_no9),
    url('news/',event_track_news),
    url('events/',event_track_event),
    url('gkg/',event_track_gkg)
]