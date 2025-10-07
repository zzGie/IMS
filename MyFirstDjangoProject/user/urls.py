from django.urls import path
from . import views


urlpatterns = [

    path('', views.index, name='index'),
    path('userlist/', views.userlist, name='userlist'),
    path('users/add/', views.adduser, name="adduser"),
    path('edituser/<int:id>/', views.edituser, name="edituser"),
    path('deleteuser/<int:id>/', views.deleteuser, name="deleteuser"),
]