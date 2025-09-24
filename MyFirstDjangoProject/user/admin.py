from django.contrib import admin
from .models import UserProfile

admin.site.site_header = "KINGKHARL"
admin.site.site_title = "Administrator Area"
admin.site.index_title = "Welcome to my First CRUD Application"


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'fullname', 'email', 'gender', 'contact_number', 'username')
    search_fields = ('fullname', 'email', 'username')
