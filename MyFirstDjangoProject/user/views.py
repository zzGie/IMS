from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.db import IntegrityError
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from .models import UserProfile, InventoryItem
from django.db.models import Sum, F, FloatField
from django.db.models.functions import Coalesce


# -------------------------------
# ✅ Dashboard / Home
# -------------------------------
def index(request):
    return render(request, "user/index.html")


# -------------------------------
# ✅ USER CRUD
# -------------------------------

# Read: Display all users
def userlist(request):
    user_list = UserProfile.objects.all()
    context = {"user_list": user_list}
    return render(request, "user/userlist.html", context)


# Create: Add new user
def adduser(request):
    if request.method == "POST":
        fullname = request.POST.get("fullname")
        email = request.POST.get("email")
        gender = request.POST.get("gender")
        contact_number = request.POST.get("contact_number")
        address = request.POST.get("address")
        username = request.POST.get("username")
        password = request.POST.get("password")
        user_image = request.FILES.get("user_image")

        try:
            user = UserProfile(
                fullname=fullname,
                email=email,
                gender=gender,
                contact_number=contact_number,
                address=address,
                username=username,
                password=make_password(password),
                user_image=user_image
            )
            user.save()
            messages.success(request, "✅ User added successfully!")
            return redirect("userlist")
        except IntegrityError:
            messages.error(request, "⚠️ Email, Contact Number, or Username already exists.")
            return redirect("adduser")

    return render(request, "user/adduser.html")


# Update: Edit user
def edituser(request, id):
    user = get_object_or_404(UserProfile, id=id)

    if request.method == "POST":
        user.fullname = request.POST.get("fullname")
        user.email = request.POST.get("email")
        user.gender = request.POST.get("gender")
        user.contact_number = request.POST.get("contact_number")
        user.address = request.POST.get("address")
        user.username = request.POST.get("username")

        if request.POST.get("password"):
            user.password = make_password(request.POST.get("password"))

        if request.FILES.get("user_image"):
            user.user_image = request.FILES.get("user_image")

        try:
            user.save()
            messages.success(request, "✅ User updated successfully!")
            return redirect("userlist")
        except IntegrityError:
            messages.error(request, "⚠️ Email or Username already exists.")
            return redirect("edituser", id=id)

    return render(request, "user/edituser.html", {"user": user})


# Delete: Remove user
def deleteuser(request, id):
    user = get_object_or_404(UserProfile, id=id)
    user.delete()
    messages.success(request, "🗑️ User deleted successfully!")
    return redirect("userlist")


# -------------------------------
# ✅ INVENTORY CRUD
# -------------------------------

# Dashboard showing stock summary
def dashboard(request):
    items = InventoryItem.objects.all()
    total_quantity = sum(item.Quantity for item in items)

    # Define thresholds
    if total_quantity < 20:
        stock_status = "Low Stock"
        stock_class = "bg-gradient-danger"
    elif total_quantity <= 100:
        stock_status = "Moderate Stock"
        stock_class = "bg-gradient-warning"
    else:
        stock_status = "High Stock"
        stock_class = "bg-gradient-success"

    context = {
        "total_quantity": total_quantity,
        "stock_status": stock_status,
        "stock_class": stock_class,
        "items": items,
    }
    return render(request, "dashboard.html", context)


# Read: Display all inventory items
def inventory_list(request):
    # Get all inventory items
    inventory_list = InventoryItem.objects.all().order_by('-DateAdded')

    # Compute total stock and total inventory value
    total_stock = sum(item.Quantity for item in inventory_list)
    total_value = sum(item.Quantity * item.Price for item in inventory_list)

    context = {
        "inventory_list": inventory_list,
        "total_stock": total_stock,
        "total_value": total_value
    }

    return render(request, "inventory/inventory_list.html", context)


# Create: Add new item
def add_inventory_item(request):
    if request.method == 'POST':
        name = request.POST.get('ItemName')
        category = request.POST.get('Category')
        quantity = request.POST.get('Quantity') or 0
        price = request.POST.get('Price') or 0
        description = request.POST.get('Description')

        try:
            InventoryItem.objects.create(
                ItemName=name,
                Category=category,
                Quantity=quantity,
                Price=price,
                Description=description
            )
            messages.success(request, '✅ Item added successfully!')
            return redirect('inventory_list')
        except Exception as e:
            messages.error(request, f'❌ Error adding item: {e}')
            return redirect('add_inventory_item')

    # ✅ Compute total stock value
    items = InventoryItem.objects.all()
    total_value = sum(item.Quantity * item.Price for item in items)

    return render(request, 'inventory/add_inventory_item.html', {
        'total_value': total_value
    })


# Update: Edit item
def edit_inventory_item(request, item_id):
    item = get_object_or_404(InventoryItem, ItemID=item_id)

    if request.method == 'POST':
        item.ItemName = request.POST.get('ItemName')
        item.Category = request.POST.get('Category')
        item.Quantity = request.POST.get('Quantity') or 0
        item.Price = request.POST.get('Price') or 0
        item.Description = request.POST.get('Description')
        item.save()
        messages.success(request, '✏️ Item updated successfully!')
        return redirect('inventory_list')

    return render(request, 'inventory/edit_inventory_item.html', {'item': item})


# Delete: Remove item
def delete_inventory_item(request, item_id):
    item = get_object_or_404(InventoryItem, ItemID=item_id)
    item.delete()
    messages.success(request, '🗑️ Item deleted successfully!')
    return redirect('inventory_list')
