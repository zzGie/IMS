from django.contrib import admin
from .models import UserProfile

# Customize admin site headers
admin.site.site_header = "KINGKHARL"
admin.site.site_title = "Administrator Area"
admin.site.index_title = "Welcome to my First CRUD Application"

# Register UserProfile with custom admin
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    # Columns to show in the list view (table)
    list_display = ('id', 'fullname', 'email', 'gender', 'contact_number', 'username')
    
    # Enable search
    search_fields = ('fullname', 'email', 'username')

    # Optional: Add filters on the sidebar
    list_filter = ('gender',)

    # Optional: Make the edit form more structured
    fieldsets = (
        ('Personal Info', {
            'fields': ('fullname', 'email', 'gender', 'contact_number')
        }),
        ('Account Info', {
            'fields': ('username', 'password')
        }),
    )
