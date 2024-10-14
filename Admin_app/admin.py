from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser,Health_Report  # Aapka custom user model

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'is_staff', 'is_active', 'is_approved')  # Aap yahan aur fields bhi add kar sakte hain
    list_filter = ('is_staff', 'is_active', 'is_approved')
    ordering = ('username',)
    
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('is_approved',)}),  # Approval field ko yahan add karein
    )

class HealthReportAdmin(admin.ModelAdmin):
    list_display = ('user', 'heart_rate', 'blood_pressure', 'spo2', 'breathing_rate', 'pro', 'hrv', 'stress', 'sympathetic_ns', 'parasympathetic_ns','current_date')  # Fields to display
    search_fields = ('user__username', 'blood_pressure')  # Fields to search
    list_filter = ('user',)  # Filter options in the admin
    ordering = ('user__username',)

admin.site.register(Health_Report, HealthReportAdmin) 
admin.site.register(CustomUser, CustomUserAdmin)
