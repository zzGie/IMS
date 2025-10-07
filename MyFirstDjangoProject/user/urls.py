from django.urls import path
from . import views

urlpatterns = [
<<<<<<< HEAD
    path('', views.index, name="index"),
    path('userlist/', views.userlist, name="userlist"),
    path('adduser/', views.adduser, name="adduser"),
]
=======

    path('', views.index, name='index'),
    path('userlist/', views.userlist, name='userlist'),
    path('users/add/', views.adduser, name="adduser"),
    path('edituser/<int:id>/', views.edituser, name="edituser"),
    path('deleteuser/<int:id>/', views.deleteuser, name="deleteuser"),
]
>>>>>>> 8f89b27653e9f1ae7b64b7470d889ba28b7a0e95
