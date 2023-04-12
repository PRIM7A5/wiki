import math
from django.urls import path

from . import views

# app_name = "encyclopedia"
urlpatterns = [
    path('new', views.createNewPage, name='new'),
    path('random', views.article, kwargs={
         "title": "", "randomPage": True}, name='random'),
    path('<str:title>/edit', views.editPage, name='edit'),
    path('<str:title>', views.article, name='title'),
    path('', views.index, name='index')
]

# urlpatterns = [
#     url(r'^$', views.post_list, name='post_list'),
#     url('r^post/(?P<pk>[0-9]+)/$', views.post_detail, name='post_detail'),
# ]
