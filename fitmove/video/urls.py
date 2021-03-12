from django.urls import path

from . import views

app_name='video'

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:room_name>/<str:name>/', views.room, name='room'),
]