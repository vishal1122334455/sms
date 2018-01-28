from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^registration/$', views.Registration.as_view(), name='registration'),
    url(r'^login/$', views.Login.as_view(), name='login'),
    url(r'^logout/$', views.logout_request, name='logout'),

    #teacher registration by office
    #url(r'^reg-teacher/$', views.RegistrationTeacher.as_view(), name='registration-teacher'),
]
