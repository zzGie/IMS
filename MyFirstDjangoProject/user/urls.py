from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('userlist/', views.userlist, name="userlist"),
    path('adduser/', views.adduser, name="adduser"),
]
