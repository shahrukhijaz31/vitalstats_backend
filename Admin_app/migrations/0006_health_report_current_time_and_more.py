# Generated by Django 4.2.15 on 2024-10-12 14:54

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Admin_app', '0005_alter_health_report_current_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='health_report',
            name='current_time',
            field=models.TimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='health_report',
            name='current_date',
            field=models.DateField(auto_now_add=True),
        ),
    ]
