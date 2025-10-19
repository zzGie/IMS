from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import IntegrityError
from django.contrib.auth.hashers import make_password, check_password
from .models import UserProfile, InventoryItem, Category  # ✅ Import Category
import json
import openpyxl
from django.http import HttpResponse
from django.db.models import Sum, Count, F

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
            request.session['user_id'] = user.id
            request.session['username'] = user.username
            request.session['fullname'] = user.fullname
            request.session['role'] = user.role
            messages.success(request, f"✅ Welcome, {user.fullname}!")
            return redirect("index")
        else:
            messages.error(request, "⚠️ Invalid username or password.")
            return redirect("login")
    return render(request, "user/login.html")

def logout_view(request):
    request.session.flush()
    messages.success(request, "You have been logged out successfully.")
    return redirect('login')

def register(request):
    """
    If a user registers with the 'admin' role, mark them as pending for confirmation.
    """
    if request.method == "POST":
        fullname = request.POST.get('fullname')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        role = request.POST.get('role')
        gender = request.POST.get('gender')
        contact_number = request.POST.get('contact_number')

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('register')
        if UserProfile.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('register')
        if UserProfile.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect('register')
        if UserProfile.objects.filter(contact_number=contact_number).exists():
            messages.error(request, "Contact number already exists.")
            return redirect('register')

        # If they selected admin, mark as pending confirmation
        is_pending_admin = False
        if role == 'admin':
            is_pending_admin = True
            role = 'pending_admin'

        user = UserProfile.objects.create(
            fullname=fullname,
            email=email,
            username=username,
            password=make_password(password),
            role=role,
            gender=gender,
            contact_number=contact_number,
            is_pending_admin=is_pending_admin
        )

        if is_pending_admin:
            messages.info(request, "🕒 Your admin request is pending approval. Wait for confirmation.")
            return redirect('confirm_admin')
        else:
            messages.success(request, "✅ Registration successful. You can now log in.")
            return redirect('login')

    return render(request, "user/register.html")

# -------------------------
# ✅ Dashboard
# -------------------------
@login_view
def index(request):
    items = InventoryItem.objects.all().order_by('Quantity')
    active_users = UserProfile.objects.count()
    low_stock_items = InventoryItem.objects.filter(Quantity__lt=10)
    low_stock = low_stock_items.count()
    high_stock = InventoryItem.objects.filter(Quantity__gte=20).count()
    total_quantity = sum(item.Quantity for item in items)

    if total_quantity < 20:
        stock_status = "Low Stock"
        stock_class = "bg-gradient-danger"
    elif total_quantity <= 50:
        stock_status = "Moderate Stock"
        stock_class = "bg-gradient-warning"
    else:
        stock_status = "High Stock"
        stock_class = "bg-gradient-success"

    if low_stock_items.exists():
        low_names = ", ".join([item.ItemName for item in low_stock_items])
        messages.warning(request, f"⚠️ Low stock alert: {low_names}")

    inventory_list = [{"name": item.ItemName, "quantity": item.Quantity} for item in items]

    context = {
        "active_users": active_users,
        "low_stock": low_stock,
        "high_stock": high_stock,
        "total_quantity": total_quantity,
        "stock_status": stock_status,
        "stock_class": stock_class,
        "inventory_list": json.dumps(inventory_list),
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
            return redirect("userlist")
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


def inventory_list(request):
    items = InventoryItem.objects.select_related('Category').all().order_by('-DateAdded')
    total_stock = items.aggregate(total=Sum('Quantity'))['total'] or 0
    total_value = items.aggregate(total=Sum(F('Quantity') * F('Price')))['total'] or 0.0

    context = {
        'inventory_list': items,
        'total_stock': total_stock,
        'total_value': total_value,
    }
    return render(request, 'inventory/inventory_list.html', context)


@login_view
def inventory_detail(request, item_id):
    item = get_object_or_404(InventoryItem, ItemID=item_id)
    return render(request, "inventory/inventory_detail.html", {"item": item})


@login_view
@admin_required
def add_inventory_item(request):
    categories = Category.objects.all()

    if request.method == "POST":
        item_name = request.POST.get("ItemName", "").strip()
        category_id = request.POST.get("Category")
        quantity = request.POST.get("Quantity")
        price = request.POST.get("Price")
        description = request.POST.get("Description", "").strip()

        # Validate required fields
        if not item_name or not price:
            messages.error(request, "Item Name and Price are required.")
            return render(request, "inventory/add_inventory_item.html", {"categories": categories})

        # Convert types safely
        try:
            quantity = int(quantity) if quantity else 0
        except ValueError:
            quantity = 0

        try:
            price = float(price)
        except ValueError:
            messages.error(request, "Invalid price format.")
            return render(request, "inventory/add_inventory_item.html", {"categories": categories})

        # Get category object if selected
        category = None
        if category_id:
            try:
                category = Category.objects.get(id=category_id)
            except Category.DoesNotExist:
                messages.warning(request, "Selected category does not exist. Item will have no category.")

        # Create item
        InventoryItem.objects.create(
            ItemName=item_name,
            Category=category,
            Quantity=quantity,
            Price=price,
            Description=description
        )

        messages.success(request, f"Item '{item_name}' added successfully!")
        return redirect("inventory_list")

    return render(request, "inventory/add_inventory_item.html", {"categories": categories})


@login_view
@admin_required
def edit_inventory_item(request, item_id):
    item = get_object_or_404(InventoryItem, ItemID=item_id)
    categories = Category.objects.all()

    if request.method == 'POST':
        item_name = request.POST.get('ItemName', '').strip()
        category_id = request.POST.get('Category')
        quantity = request.POST.get('Quantity', 0)
        price = request.POST.get('Price', 0)
        description = request.POST.get('Description', '').strip()

        # Safe conversions
        try:
            quantity = int(quantity)
        except ValueError:
            quantity = 0

        try:
            price = float(price)
        except ValueError:
            price = 0.0

        category = None
        if category_id:
            try:
                category = Category.objects.get(id=category_id)
            except Category.DoesNotExist:
                category = None

        # Update item
        item.ItemName = item_name
        item.Category = category
        item.Quantity = quantity
        item.Price = price
        item.Description = description
        item.save()

        messages.success(request, '✏️ Item updated successfully!')
        return redirect('inventory_list')

    return render(request, 'inventory/edit_inventory_item.html', {'item': item, 'categories': categories})


@login_view
@admin_required
def delete_inventory_item(request, item_id):
    item = get_object_or_404(InventoryItem, ItemID=item_id)
    item.delete()
    messages.success(request, '🗑️ Item deleted successfully!')
    return redirect('inventory_list')
# -------------------------
# ✅ Category CRUD
# -------------------------
@login_view
def category_list(request):
    categories = Category.objects.all().order_by('name')  # or 'category_name' depending on your model
    return render(request, 'category/category_list.html', {'category_list': categories})


@login_view
@admin_required
def add_category(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        if Category.objects.filter(name=name).exists():
            messages.error(request, f"⚠️ Category '{name}' already exists.")
            return redirect('add_category')
        Category.objects.create(name=name, description=description)
        messages.success(request, f"✅ Category '{name}' added successfully!")
        return redirect('category_list')
    return render(request, 'category/add_category.html')

@login_view
@admin_required
def edit_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.method == 'POST':
        name = request.POST.get('category_name')  # match your template
        description = request.POST.get('description')

        if Category.objects.filter(name=name).exclude(id=category_id).exists():
            messages.error(request, f"⚠️ Category '{name}' already exists.")
            return redirect('edit_category', category_id=category_id)

        category.name = name
        category.description = description
        category.save()
        messages.success(request, f"✏️ Category '{name}' updated successfully!")
        return redirect('category_list')

    return render(request, 'category/edit_category.html', {'category': category})

@login_view
@admin_required
def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    category_name = category.name
    category.delete()
    messages.success(request, f"🗑️ Category '{category_name}' deleted successfully!")
    return redirect('category_list')

# -------------------------
# ✅ Reports & Excel Export
# -------------------------

@login_view
@admin_required
def reports_dashboard(request):
    # Total inventory stats
    total_items = InventoryItem.objects.count()
    total_quantity = InventoryItem.objects.aggregate(total_qty=Sum('Quantity'))['total_qty'] or 0
    total_value = InventoryItem.objects.aggregate(total_value=Sum(F('Quantity') * F('Price')))['total_value'] or 0

    # Category-wise stats
    category_stats = (
        InventoryItem.objects
        .values('Category__name')  # <-- fixed field name
        .annotate(
            total_items=Count('ItemID'),
            total_quantity=Sum('Quantity'),
            total_value=Sum(F('Quantity') * F('Price'))
        )
        .order_by('Category__name')
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
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Inventory"

    # Header row
    ws.append(["ItemID", "ItemName", "Category", "Quantity", "Price"])

    # Data rows
    for item in InventoryItem.objects.select_related('Category').all():
        ws.append([
            item.ItemID,
            item.ItemName,
            item.Category.name if item.Category else "",  # <-- fixed field name
            item.Quantity,
            float(item.Price)
        ])

    # Response
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=inventory.xlsx'
    wb.save(response)
    return response

# -------------------------
# ✅ Admin Confirmation
# -------------------------
@login_view
@admin_required
def confirm_admin(request):
    """
    Show all users requesting admin access.
    Approve or decline them.
    """
    if request.method == "POST":
        user_id = request.POST.get("user_id")
        action = request.POST.get("action")
        try:
            user = UserProfile.objects.get(id=user_id)
            if action == "accept":
                user.role = "admin"
                user.is_pending_admin = False
                user.save()
                messages.success(request, f"✅ {user.fullname} is now an admin!")
            elif action == "decline":
                user.role = "user"
                user.is_pending_admin = False
                user.save()
                messages.warning(request, f"❌ {user.fullname}'s admin request was declined.")
        except UserProfile.DoesNotExist:
            messages.error(request, "⚠️ User not found.")
        return redirect("confirm_admin")

    pending_users = UserProfile.objects.filter(is_pending_admin=True)
    return render(request, "user/confirm_admin.html", {"pending_users": pending_users})
