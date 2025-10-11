from django.urls import path
from . import views

urlpatterns = [
    # 🔐 Root redirected to login
    path('', views.login, name='login'),

    # 🏠 Dashboard / Index
    path('index/', views.index, name='index'),

    # 👤 User CRUD
    path('userlist/', views.userlist, name='userlist'),
    path('users/add/', views.adduser, name="adduser"),
    path('edituser/<int:id>/', views.edituser, name="edituser"),
    path('deleteuser/<int:id>/', views.deleteuser, name="deleteuser"),

    # 📦 Inventory CRUD
    path('inventory/', views.inventory_list, name='inventory_list'),
    path('inventory/add/', views.add_inventory_item, name='add_inventory_item'),
    path('inventory/edit/<int:item_id>/', views.edit_inventory_item, name='edit_inventory_item'),
    path('inventory/delete/<int:item_id>/', views.delete_inventory_item, name='delete_inventory_item'),

    # 🔐 Authentication
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
