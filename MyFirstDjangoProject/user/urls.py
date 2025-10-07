from django.urls import path
from . import views

urlpatterns = [
    # 🏠 Home
    path('', views.index, name='index'),

    # 👤 User CRUD
    path('userlist/', views.userlist, name='userlist'),            # Read
    path('users/add/', views.adduser, name="adduser"),             # Create
    path('edituser/<int:id>/', views.edituser, name="edituser"),   # Update
    path('deleteuser/<int:id>/', views.deleteuser, name="deleteuser"),  # Delete

    # 📦 Inventory CRUD
    path('inventory/', views.inventory_list, name='inventory_list'),                       # Read
    path('inventory/add/', views.add_inventory_item, name='add_inventory_item'),           # Create
    path('inventory/edit/<int:item_id>/', views.edit_inventory_item, name='edit_inventory_item'),  # Update
    path('inventory/delete/<int:item_id>/', views.delete_inventory_item, name='delete_inventory_item'), # Delete
]
