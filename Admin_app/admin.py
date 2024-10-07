from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser  # Aapka custom user model

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'is_staff', 'is_active', 'is_approved')  # Aap yahan aur fields bhi add kar sakte hain
    list_filter = ('is_staff', 'is_active', 'is_approved')
    ordering = ('username',)
    
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('is_approved',)}),  # Approval field ko yahan add karein
    )
admin.site.register(CustomUser, CustomUserAdmin)
