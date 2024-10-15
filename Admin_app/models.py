from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class CustomUser(AbstractUser):
    user_role = models.CharField(max_length=50, null=True, blank=True)
    is_approved = models.BooleanField(default=False)

# Health_Report model
class Health_Report(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # ForeignKey to CustomUser
    pulse_rate = models.CharField(max_length=20)
    blood_pressure = models.CharField(max_length=20)  # Systolic/Diastolic format
    mean_rri = models.CharField(max_length=20)  # Blood oxygen level (SpO2)
    oxygen_saturation = models.CharField(max_length=20)
    hemoglobin = models.CharField(max_length=20)  # PRO field
    hrhemoglobin_a1cv = models.CharField(max_length=20)  # Heart Rate Variability (HRV)
    lfhf = models.CharField(max_length=20)
    pns_index = models.CharField(max_length=20)  # Sympathetic Nervous System
    pns_zone = models.CharField(max_length=20)  # Parasympathetic Nervous System
    prq = models.CharField(max_length=20)
    rmssd = models.CharField(max_length=20)
    respiration_rate = models.CharField(max_length=20)
    sd1 = models.CharField(max_length=20)
    sd2 = models.CharField(max_length=20)
    sdnn = models.CharField(max_length=20)
    sns_index = models.CharField(max_length=20)
    sns_zone = models.CharField(max_length=20)
    stress_level = models.CharField(max_length=20)
    stress_index = models.CharField(max_length=20)
    wellness_index = models.CharField(max_length=20)
    wellness_level = models.CharField(max_length=20)
    current_date = models.DateField(auto_now_add=True)  # Automatically add current date
    current_time = models.TimeField(auto_now_add=True)  # Automatically add current time

    def __str__(self):
        return f"Health Report for {self.user.username}"