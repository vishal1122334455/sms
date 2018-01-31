from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.Home.as_view(), name='index'),
    url(r'^office-registration/$', views.Registration.as_view(), name='office-registration'),
]
