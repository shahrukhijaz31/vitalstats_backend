from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser,Health_Report  # Aapka custom user model

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'is_staff', 'is_active', 'is_approved', 'user_role')  # Aap yahan aur fields bhi add kar sakte hain
    list_filter = ('is_staff', 'is_active', 'is_approved')
    ordering = ('username',)
    
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('is_approved',)}),  # Approval field ko yahan add karein
    )

class HealthReportAdmin(admin.ModelAdmin):
    list_display = ('user', 'pulse_rate', 'blood_pressure', 'mean_rri', 'oxygen_saturation',
                    'hemoglobin', 'hrhemoglobin_a1cv', 'lfhf', 'pns_index', 'pns_zone','rmssd',
                    'respiration_rate','sd1','sd2','sdnn','sns_index','sns_zone',
                    'stress_level','stress_index','wellness_index','wellness_level','current_date','current_time')  # Fields to display
    search_fields = ('user__username', 'blood_pressure')  # Fields to search
    list_filter = ('user',)  # Filter options in the admin
    ordering = ('user__username',)

admin.site.register(Health_Report, HealthReportAdmin) 
admin.site.register(CustomUser, CustomUserAdmin)
