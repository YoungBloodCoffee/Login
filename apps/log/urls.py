from django.conf.urls import url
from . import views


urlpatterns = [
  url(r'^$', views.index),
  url(r'^login$', views.login),
  url(r'^process$', views.process),
  url(r'^success$', views.success),
  url(r'^log$', views.log),
  url(r'^(?P<id>\d+)/remove$', views.remove)
  ]