from django.db import models
from django.db import models
#from datetime import datetime
#from django.contrib.auth.models import User

# Create your models here.
class Employee(models.Model):
    full_name = models.CharField(max_length=150)
    email = models.EmailField(max_length=150)
    address = models.CharField(max_length=150)
    gender = models.CharField(max_length=50)
    contact = models.CharField(max_length=150)
   
    def __str__(self):
        return self.full_name
    
    class Meta:
        db_table = "app_employee"
    
class Payroll(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    bonus = models.DecimalField(max_digits=10, decimal_places=2)
    taxes = models.DecimalField(max_digits=10, decimal_places=2)
    other_deduction = models.DecimalField(max_digits=10, decimal_places=2)
    net_salary = models.DecimalField(max_digits=10, decimal_places=2)
    pay_period_start= models.DateField()
    pay_period_end = models.DateField()
    status = models.BooleanField(default=False)

    def __str__(self):
        return str(self.employee)
    
    class Meta:
        db_table = "app_payroll"

class Attendance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField()
    time_in = models.TimeField()
    time_out = models.TimeField()
    hours_worked = models.DurationField()
    status = models.BooleanField(default=False)
    def __str__(self):
        return str(self.employee)
    
    class Meta:
        db_table = "app_attendance"