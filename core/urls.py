from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('upload/', views.upload_json, name='upload_json'),
    path('records/', views.records_table, name='records_table'),
]
