# Generated by Django 4.1.7 on 2023-03-10 03:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_payroll', '0004_alter_attendance_date_alter_attendance_time_in_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payroll',
            name='employee',
        ),
        migrations.DeleteModel(
            name='Attendance',
        ),
        migrations.DeleteModel(
            name='Employee',
        ),
        migrations.DeleteModel(
            name='Payroll',
        ),
    ]
