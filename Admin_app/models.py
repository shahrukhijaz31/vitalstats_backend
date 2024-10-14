from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class CustomUser(AbstractUser):
    user_role = models.CharField(max_length=20)
    is_approved = models.BooleanField(default=False)

# Health_Report model
class Health_Report(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # ForeignKey to CustomUser
    heart_rate = models.CharField(max_length=20)
    blood_pressure = models.CharField(max_length=20)  # Systolic/Diastolic format
    spo2 = models.CharField(max_length=20)  # Blood oxygen level (SpO2)
    breathing_rate = models.CharField(max_length=20)
    pro = models.CharField(max_length=20)  # PRO field
    hrv = models.CharField(max_length=20)  # Heart Rate Variability (HRV)
    stress = models.CharField(max_length=20)
    sympathetic_ns = models.CharField(max_length=20)  # Sympathetic Nervous System
    parasympathetic_ns = models.CharField(max_length=20)  # Parasympathetic Nervous System
    current_date = models.DateField(auto_now_add=True)  # Automatically add current date
    current_time = models.TimeField(auto_now_add=True)  # Automatically add current time

    def __str__(self):
        return f"Health Report for {self.user.username}"