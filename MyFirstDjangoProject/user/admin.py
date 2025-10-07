from django.contrib import admin
from .models import UserProfile, InventoryItem

# ✅ Customize admin site headers
admin.site.site_header = "ADMINISTRATION"
admin.site.site_title = "Administrator Area"
admin.site.index_title = "Welcome to My First CRUD Application"


# ✅ UserProfile Admin
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'fullname',
        'email',
        'gender',
        'contact_number',
        'image_tag',
        'username'
    )
    search_fields = ('fullname', 'email', 'username', 'contact_number')
    list_filter = ('gender',)
    fieldsets = (
        ('Personal Information', {
            'fields': ('fullname', 'email', 'gender', 'contact_number', 'address', 'user_image', 'image_tag')
        }),
        ('Account Information', {
            'fields': ('username', 'password')
        }),
    )
    readonly_fields = ('image_tag',)


# ✅ InventoryItem Admin
@admin.register(InventoryItem)
class InventoryItemAdmin(admin.ModelAdmin):
    list_display = ('ItemID', 'ItemName', 'Category', 'Quantity', 'Price', 'DateAdded')
    search_fields = ('ItemName', 'Category')
    list_filter = ('Category',)
    ordering = ('-DateAdded',)  # Newest first

    fieldsets = (
        ('Item Information', {
            'fields': ('ItemName', 'Category', 'Quantity', 'Price', 'Description')
        }),
        ('System Fields', {
            'fields': ('DateAdded',),
        }),
    )
    readonly_fields = ('DateAdded',)
