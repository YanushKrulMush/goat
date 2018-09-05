from django.urls import path, re_path
from . import views

urlpatterns = [
    re_path(r'(\d+)/$', views.view_list, name='view_list'),
    re_path(r'(\d+)/add_item$', views.add_item, name='add_item'),
    path('new', views.new_list, name='new_list')
]