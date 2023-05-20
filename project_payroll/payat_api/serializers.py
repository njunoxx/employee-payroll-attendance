from rest_framework import serializers
from app_payroll.models import Employee, Payroll, Attendance
from django.contrib.auth.models import User

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ("id", "full_name", "email", "address", "gender", "contact")

class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = ("id", "employee", "status", "date", "time_in", "time_out", "hours_worked")

class PayrollSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payroll
        fields = ("id", "employee", "salary", "bonus","status", "taxes", "other_deduction", "net_salary", "pay_period_start", "pay_period_end")
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "password", "email")
        extra_kwargs = {'password': {'write_only':True}}

        # def create(self, validated_data):
        #     user = User(
        #         email=validated_data['email'],
        #         username=validated_data['username'],
        #         password = validated_data['password']
        #     )
        #     return user