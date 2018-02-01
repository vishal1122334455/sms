from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.Home.as_view(), name='index'),

    #::::start member operation module url::::
    #:::::::::::::::::::::::::::::::::::::::::
    url(r'^office-registration/$', views.Registration.as_view(), name='office-registration'),

    #member operations
    url(r'^member/search/$', views.MemberSearch.as_view(), name='member-search'),

    #list of member
    url(r'^member/list/$', views.MemberList.as_view(), name='member-list'),
    url(r'^member/list/(?P<type>[a-zA-Z]+)/$', views.MemberListDetail.as_view(), name='member-list-detail'),

    #list of class in student
    url(r'^member/list/student/class/$', views.StudentClass.as_view(), name='student-class'),
    url(r'^member/list/student/class/(?P<classes>[a-zA-Z0-9]+)/$', views.StudenListInClass.as_view(), name='student-list-in-class'),

    #list of section in class
    url(r'^member/list/student/class/(?P<classes>[a-zA-Z0-9]+)/section/$', views.ClassWiseSection.as_view(), name='section'),
    url(r'^member/list/student/class/(?P<classes>[a-zA-Z0-9]+)/section/(?P<section>[a-zA-Z0-9-_]+)/$', views.SectionWiseStudent.as_view(), name='section-wise-student'),


    url(r'^member/detail/(?P<pk>[0-9]+)/$', views.MemberDetail.as_view(), name='member-detail'),
    url(r'^member/edit/(?P<pk>[0-9]+)/$', views.MemberEdit.as_view(), name='member-edit'),
    url(r'^member/delete/(?P<pk>[0-9]+)/$', views.MemberDelete.as_view(), name='member-delete'),
    #:::::::::::::::::::::::::::::::::::::::
    #::::end member operation module url::::


    #::::start schedule module url::::
    #:::::::::::::::::::::::::::::::::


    url(r'^schedule/$', views.Schedule.as_view(), name='schedule'),
    url(r'^schedule/class-list/$', views.ClassList.as_view(), name='class-list'),
    url(r'^schedule/class-list/(?P<classes>[a-zA-Z0-9]+)/$', views.SectionList.as_view(), name='section-list'),


    #::::start schedule module url::::
    #:::::::::::::::::::::::::::::::::

]
