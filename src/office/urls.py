from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.Home.as_view(), name='index'),
    url(r'^office-registration/$', views.Registration.as_view(), name='office-registration'),

    #member operations
    url(r'^member/search/$', views.MemberSearch.as_view(), name='member-search'),
    url(r'^member/detail/(?P<pk>[0-9]+)/$', views.MemberDetail.as_view(), name='member-detail'),
    url(r'^member/edit/(?P<pk>[0-9]+)/$', views.MemberEdit.as_view(), name='member-edit'),
    url(r'^member/delete/(?P<pk>[0-9]+)/$', views.MemberDelete.as_view(), name='member-delete'),
]
