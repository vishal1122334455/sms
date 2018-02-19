from django.conf.urls import url

from . import views



urlpatterns = [
    url(r'^$', views.Home.as_view(), name='index'),

    #::::start schedule module url::::
    #:::::::::::::::::::::::::::::::::


    url(r'^schedule/$', views.Schedule.as_view(), name='schedule'),

    url(r'^schedule/class-list/routine/view/$', views.RoutineView.as_view(), name='routine-view'),

    url(r'^schedule/class-list/exam-routine/view/$', views.ExamRoutineView.as_view(), name='exam-routine-view'),
    url(r'^schedule/class-list/class-test-routine/view/$', views.ClassTestRoutineView.as_view(), name='class-test-routine-view'),


    #::::end schedule module url::::
    #:::::::::::::::::::::::::::::::::
]
