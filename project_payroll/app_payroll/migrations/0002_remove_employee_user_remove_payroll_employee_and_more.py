# Generated by Django 4.1.7 on 2023-03-10 03:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_payroll', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='user',
        ),
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
