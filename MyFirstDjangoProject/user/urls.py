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
    path('inventory/<int:item_id>/', views.inventory_detail, name='inventory_detail'),
    path('inventory/edit/<int:item_id>/', views.edit_inventory_item, name='edit_inventory_item'),
    path('inventory/delete/<int:item_id>/', views.delete_inventory_item, name='delete_inventory_item'),

      path('categories/', views.category_list, name='category_list'),
      path('categories/add/', views.add_category, name='add_category'),
      path('categories/edit/<int:category_id>/', views.edit_category, name='edit_category'),
      path('categories/delete/<int:category_id>/', views.delete_category, name='delete_category'),


    # 📊 Reports
    path('reports/', views.reports_dashboard, name='reports_dashboard'),
    path('export_inventory_excel/', views.export_inventory_excel, name='export_inventory_excel'),

    # 🔐 Authentication
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # ⚙️ Admin Confirmation
    path('confirm-admin/', views.confirm_admin, name='confirm_admin'),
]
