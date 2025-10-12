from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import IntegrityError
from django.contrib.auth.hashers import make_password, check_password
from .models import UserProfile, InventoryItem
import json
from django.core import serializers
import openpyxl
from django.http import HttpResponse
from django.db.models import Sum, Count
# -------------------------
# ✅ Custom Decorators
# -------------------------
def login_view(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.session.get('user_id'):
            messages.error(request, "⚠️ Please log in first.")
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper

def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.session.get('role') != 'admin':
            messages.error(request, "⚠️ You do not have permission to access this page.")
            return redirect('index')
        return view_func(request, *args, **kwargs)
    return wrapper

# -------------------------
# ✅ Authentication
# -------------------------
def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            user = UserProfile.objects.get(username=username)
        except UserProfile.DoesNotExist:
            messages.error(request, "⚠️ Invalid username or password.")
            return redirect("login")

        if check_password(password, user.password):
            # ✅ Save important user info in session
            request.session['user_id'] = user.id
            request.session['username'] = user.username
            request.session['fullname'] = user.fullname     # 👈 Added this line
            request.session['role'] = user.role

            messages.success(request, f"✅ Welcome, {user.fullname}!")
            return redirect("index")
        else:
            messages.error(request, "⚠️ Invalid username or password.")
            return redirect("login")

    return render(request, "user/login.html")


def logout_view(request):
    
    messages.success(request, "You have been logged out successfully.")
    return redirect('login')  # Redirect to login page

def register(request):
    if request.method == "POST":
        fullname = request.POST.get('fullname')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        role = request.POST.get('role')
        gender = request.POST.get('gender')
        contact_number = request.POST.get('contact_number')

        # Password match check
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('register')

        # Check for duplicates
        if UserProfile.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('register')
        if UserProfile.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect('register')
        if UserProfile.objects.filter(contact_number=contact_number).exists():
            messages.error(request, "Contact number already exists.")
            return redirect('register')

        # Save user
        user = UserProfile(
            fullname=fullname,
            email=email,
            username=username,
            password=make_password(password),
            role=role,
            gender=gender,
            contact_number=contact_number
        )
        user.save()
        messages.success(request, "Registration successful. You can now login.")
        return redirect('login')

    return render(request, "user/register.html")

# -------------------------
# ✅ Dashboard
# -------------------------
@login_view
def index(request):
    # ✅ Fetch and sort items (Low → High Quantity)
    items = InventoryItem.objects.all().order_by('Quantity')

    # ✅ Get stats
    active_users = UserProfile.objects.count()
    low_stock_items = InventoryItem.objects.filter(Quantity__lt=10)  # FIXED
    low_stock = low_stock_items.count()
    high_stock = InventoryItem.objects.filter(Quantity__gte=20).count()
    total_quantity = sum(item.Quantity for item in items)

    # ✅ Stock status
    if total_quantity < 20:
        stock_status = "Low Stock"
        stock_class = "bg-gradient-danger"
    elif total_quantity <= 50:
        stock_status = "Moderate Stock"
        stock_class = "bg-gradient-warning"
    else:
        stock_status = "High Stock"
        stock_class = "bg-gradient-success"

    # ✅ Low stock alert message
    if low_stock_items.exists():
        low_names = ", ".join([item.ItemName for item in low_stock_items])
        messages.warning(request, f"⚠️ Low stock alert: {low_names}")

    # ✅ Chart data for JavaScript
    inventory_list = [
        {"name": item.ItemName, "quantity": item.Quantity} for item in items
    ]

    context = {
        "active_users": active_users,
        "low_stock": low_stock,
        "high_stock": high_stock,
        "total_quantity": total_quantity,
        "stock_status": stock_status,
        "stock_class": stock_class,
        "inventory_list": json.dumps(inventory_list),  # ✅ JSON-safe for JS
        "items": items,
    }

    return render(request, "user/index.html", context)
# -------------------------
# ✅ User CRUD
# -------------------------
@login_view

def userlist(request):
    return render(request, "user/userlist.html", {"user_list": UserProfile.objects.all()})

@login_view
@admin_required
def adduser(request):
    if request.method == "POST":
        try:
            user = UserProfile(
                fullname=request.POST.get("fullname"),
                email=request.POST.get("email"),
                gender=request.POST.get("gender"),
                contact_number=request.POST.get("contact_number"),
                address=request.POST.get("address"),
                username=request.POST.get("username"),
                password=make_password(request.POST.get("password")),
                user_image=request.FILES.get("user_image")
            )
            user.save()
            messages.success(request, "✅ User added successfully!")
            return redirect("userlist")  # 👈 Redirects to userlist after saving
        except IntegrityError:
            messages.error(request, "⚠️ Email, Contact Number, or Username already exists.")
            return redirect("adduser")
    return render(request, "user/adduser.html")

@login_view
@admin_required
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

@login_view
@admin_required
def deleteuser(request, id):
    get_object_or_404(UserProfile, id=id).delete()
    messages.success(request, "🗑️ User deleted successfully!")
    return redirect("userlist")

# -------------------------
# ✅ Inventory CRUD
# -------------------------
@login_view
def inventory_list(request):
    inventory_list = InventoryItem.objects.all().order_by('-DateAdded')
    total_stock = sum(item.Quantity for item in inventory_list)
    total_value = sum(item.Quantity * item.Price for item in inventory_list)
    return render(request, "inventory/inventory_list.html", {"inventory_list": inventory_list, "total_stock": total_stock, "total_value": total_value})

@login_view
def inventory_detail(request, item_id):
    # Fetch the inventory item by its primary key (ItemID)
    item = get_object_or_404(InventoryItem, ItemID=item_id)
    return render(request, "inventory/inventory_detail.html", {"item": item})


@login_view
@admin_required
def add_inventory_item(request):
    if request.method == 'POST':
        try:
            InventoryItem.objects.create(
                ItemName=request.POST.get('ItemName'),
                Category=request.POST.get('Category'),
                Quantity=request.POST.get('Quantity') or 0,
                Price=request.POST.get('Price') or 0,
                Description=request.POST.get('Description')
            )
            messages.success(request, '✅ Item added successfully!')
            return redirect('inventory_list')
        except Exception as e:
            messages.error(request, f'❌ Error adding item: {e}')
            return redirect('add_inventory_item')
    return render(request, 'inventory/add_inventory_item.html')

@login_view

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

@login_view
@admin_required
def delete_inventory_item(request, item_id):
    get_object_or_404(InventoryItem, ItemID=item_id).delete()
    messages.success(request, '🗑️ Item deleted successfully!')
    return redirect('inventory_list')

@login_view
@admin_required
def category_list(request):
    categories = InventoryItem.objects.all()
    return render(request, 'inventory/category_list.html', {'categories': categories})

@login_view
@admin_required
def reports_dashboard(request):
    from django.db.models import Sum, Count

    total_items = InventoryItem.objects.count()
    total_quantity = InventoryItem.objects.aggregate(Sum('Quantity'))['Quantity__sum'] or 0
    total_value = InventoryItem.objects.aggregate(total=Sum('Price'))['total'] or 0

    category_stats = (
        InventoryItem.objects
        .values('Category')
        .annotate(total_items=Count('id'), total_quantity=Sum('Quantity'))
        .order_by('Category')
    )

    context = {
        'total_items': total_items,
        'total_quantity': total_quantity,
        'total_value': total_value,
        'category_stats': category_stats,
    }

    return render(request, 'reports/reports_dashboard.html', context)


@login_view
@admin_required
def reports_dashboard(request):
    from django.db.models import Sum, Count, F

    # ✅ Summary Totals
    total_items = InventoryItem.objects.count()
    total_quantity = InventoryItem.objects.aggregate(total_qty=Sum('Quantity'))['total_qty'] or 0
    total_value = InventoryItem.objects.aggregate(
        total_value=Sum(F('Quantity') * F('Price'))
    )['total_value'] or 0

    # ✅ Category Breakdown
    category_stats = (
        InventoryItem.objects
        .values('Category')
        .annotate(
            total_items=Count('ItemID'),
            total_quantity=Sum('Quantity'),
            total_value=Sum(F('Quantity') * F('Price'))
        )
        .order_by('Category')
    )

    context = {
        'total_items': total_items,
        'total_quantity': total_quantity,
        'total_value': total_value,
        'category_stats': category_stats,
    }

    return render(request, 'reports/reports_dashboard.html', context)



@login_view
@admin_required
def export_inventory_excel(request):
    # Create an Excel workbook
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Inventory"

    # Add header row
    ws.append(["ItemID", "ItemName", "Quantity", "Price"])  # Adjust columns

    # Add data
    for item in InventoryItem.objects.all():
        ws.append([item.ItemID, item.ItemName, item.Quantity, item.Price])

    # Prepare response
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=inventory.xlsx'
    wb.save(response)
    return response