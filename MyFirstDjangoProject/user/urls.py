from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_list, name='user_list'),
    path('add/', views.user_create, name='user_add'),
    path('<int:pk>/', views.user_detail, name='user_detail'),
]
