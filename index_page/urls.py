from django.contrib import admin
from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.frontpage),
    path('song_detail/<str:song_name>/<str:singer_name>/<str:list_name>', views.index, name="song_detail")
]