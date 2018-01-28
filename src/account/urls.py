from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^registration/$', views.Registration.as_view(), name='registration'),
]
