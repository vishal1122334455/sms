from django.conf.urls import url

from . import views



urlpatterns = [
    url(r'^$', views.Home.as_view(), name='index'),

    #attendance module start
    url(r'^attendance/class-list/$', views.AttendanceClassList.as_view(), name='attendance-class-list'),
    url(r'^attendance/(?P<classes>[a-zA-Z0-9-_]+)/section-list/$', views.AttendanceSectionList.as_view(), name='attendance-section-list'),
    url(r'^attendance/(?P<classes>[a-zA-Z0-9-_]+)/(?P<section>[a-zA-Z0-9-_]+)/subject-list/$', views.AttendanceSubjectList.as_view(), name='attendance-subject-list'),
    url(r'^attendance/(?P<classes>[a-zA-Z0-9-_]+)/(?P<section>[a-zA-Z0-9-_]+)/(?P<subject_id>[0-9]+)/all/$', views.AttendanceSubjectAll.as_view(), name='attendance-subject-all'),
    url(r'^attendance/(?P<classes>[a-zA-Z0-9-_]+)/(?P<section>[a-zA-Z0-9-_]+)/(?P<attendance_id>[0-9]+)/create/$', views.AttendanceCreate.as_view(), name='attendance-create'),
    url(r'^attendance/(?P<classes>[a-zA-Z0-9-_]+)/(?P<section>[a-zA-Z0-9-_]+)/(?P<subject_id>[0-9]+)/statistics/$', views.AttendanceSubjectWiseStatistics.as_view(), name='attendance-subject-wise-statistics'),

    #:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    #::::::::::::::::::::::::::::::::api::::::::::::::::::::::::::::
    #:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

    url(r'^attendance/api/$', views.AttendanceAPIPresent.as_view(), name='attendence-api'),

]
