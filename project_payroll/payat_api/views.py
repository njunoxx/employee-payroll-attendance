from django.shortcuts import render
from .serializers import EmployeeSerializer, AttendanceSerializer, PayrollSerializer, UserSerializer
from app_payroll.models import Employee, Attendance, Payroll
from datetime import datetime, date

from django.contrib import auth
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User

from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from rest_framework.views import APIView

from django.http import HttpResponse
from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter


# Create your views here.
class CustomResponse():
    def successResponse(self, code, msg, data=dict()):
        context = {
            "status_code" : code,
            "message" : msg,
            "data" : data,
            "error" : []
        }
        return context
    


class EmployeeApiView(APIView):
    def get(self, request):
        employee = Employee.objects.all()
        serializer = EmployeeSerializer(employee, many=True)
        return Response(CustomResponse.successResponse(200, "Employee Lists", serializer.data), status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(CustomResponse.successResponse(200, "Added Successfully", serializer.data), status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class EmployeeApiIdView(APIView):
    def get_object(self, id):
        try:
            data = Employee.objects.get(id=id)
            return data
        except Employee.DoesNotExist:
            return None
        
    def get(self, request, id):
        instance = self.get_object(id)
        if not instance:
            return Response({"msg":"Not Found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = EmployeeSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id):
        instance = self.get_object(id)
        if not instance:
            return Response({"msg":"Not Found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = EmployeeSerializer(data=request.data, instance=instance)
        if serializer.is_valid():
            serializer.save()
            return Response(CustomResponse.successResponse(200, "Added Successfully", serializer.data), status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        instance = self.get_object(id)
        if not instance:
            return Response({"msg":"Not Found"}, status=status.HTTP_404_NOT_FOUND)
        instance.delete()
        return Response({"msg":"Deleted Successfully"}, status=status.HTTP_200_OK)



class AttendanceApiView(APIView):
    def get(self, request):
        attendance = Attendance.objects.all()
        serializer =  AttendanceSerializer(attendance, many=True)
        return Response(CustomResponse.successResponse(200, "Attendance Lists", serializer.data), status=status.HTTP_200_OK)

    def post(self, request):
        attendance_date = request.POST.get('date')
        if attendance_date < str(date.today()) or attendance_date > str(date.today()):
            return Response({"msg":"You have entered either Past or Future Date."}, status=status.HTTP_403_FORBIDDEN)
        else:
            time_in1 = request.POST.get('time_in')
            time_out1 = request.POST.get('time_out')
            time_format = "%H:%M:%S.%f"
            time_in = datetime.strptime(time_in1, time_format)
            time_out = datetime.strptime(time_out1, time_format)
            hours_worked = (time_out - time_in).total_seconds()/3600
            data = {
                "employee" : request.POST.get('employee'),
                "date" : request.POST.get('date'),
                "time_in": time_in1,
                "time_out": time_out1,
                "hours_worked": hours_worked,
                "status" : True if request.POST.get("status")=="status" else False
            }
            status1 = Attendance.objects.filter(status=True,
                                                employee=request.POST.get('employee'),
                                                date=request.POST.date
                                                )
            if status1.exists():
                return Response({"msg":"Attendance for today has already been recorded."}, status=status.HTTP_406_NOT_ACCEPTABLE)
            else:
                serializer = AttendanceSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(CustomResponse.successResponse(200, "Added Successfully", serializer.data), status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class AttendanceApiIdView(APIView):
    def get_object(self, id):
        try:
            data = Attendance.objects.get(id=id)
            return data
        except Attendance.DoesNotExist:
            return None
        
    def get(self, request, id):
        instance = self.get_object(id)
        if not instance:
            return Response({"msg":"Not Found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = AttendanceSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, id):
        instance = self.get_object(id)
        if not instance:
            return Response({"msg":"Not Found"}, status=status.HTTP_404_NOT_FOUND)
        
        attendance_date = request.POST.get('date')
        if attendance_date < str(date.today()) or attendance_date > str(date.today()):
            return Response({"msg":"You have entered either Past or Future Date."}, status=status.HTTP_403_FORBIDDEN)
        else:
            time_in1 = request.POST.get('time_in')
            time_out1 = request.POST.get('time_out')
            time_format = "%H:%M:%S.%f"
            time_in = datetime.strptime(time_in1, time_format)
            time_out = datetime.strptime(time_out1, time_format)
            hours_worked = (time_out - time_in).total_seconds()/3600
            data = {
                "employee" : request.POST.get('employee'),
                "date" : request.POST.get('date'),
                "time_in": time_in1,
                "time_out": time_out1,
                "hours_worked": hours_worked,
            }
        serializer = AttendanceSerializer(data=data, instance=instance)
        if serializer.is_valid():
            serializer.save()
            return Response(CustomResponse.successResponse(200, "Added Successfully", serializer.data), status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id):
        instance = self.get_object(id)
        if not instance:
            return Response({"msg":"Not Found"}, status=status.HTTP_404_NOT_FOUND)
        instance.delete()
        return Response({"msg":"Deleted Successfully"}, status=status.HTTP_200_OK)
    

    
class PayrollApiView(APIView):
    def get(self, request):
        pay = Payroll.objects.all()
        serializer = PayrollSerializer(pay, many=True)
        return Response(CustomResponse.successResponse(200, "Payroll List", serializer.data), status=status.HTTP_200_OK)

    def post(self, request):
        salary1 = request.POST.get('salary')
        bonus1 = request.POST.get('bonus')
        taxes1 = request.POST.get('taxes')
        other_deduction1 = request.POST.get('other_deduction')
        pay_period_start = request.POST.get('pay_period_start')

        salary = float(salary1)
        bonus = float(bonus1)
        taxes = float(taxes1)
        other_deduction = float(other_deduction1)
        net_salary = (salary+bonus)-(taxes+other_deduction)

        data = {
            "employee" : request.POST.get('employee'),
            "pay_period_start" : request.POST.get('pay_period_start'),
            "pay_period_end" : request.POST.get('pay_period_end'),
            "salary" : salary1,
            "bonus" : bonus1,
            "taxes" : taxes1,
            "other_deduction" : other_deduction1,
            "status" : True if request.POST.get("status")=="status" else False,
            "net_salary" : net_salary
        }
        status1 = Payroll.objects.filter(status=True,
                                        employee=request.POST.get('employee'),
                                        pay_period_start__year=pay_period_start[:4], 
                                        pay_period_start__month=request.POST.get('pay_period_start')[5:7]
                                        )
        if status1.exists():
            return Response({"msg":"Payroll Data already exists for entered Year and Month."}, status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            serializer = PayrollSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(CustomResponse.successResponse(200, "Added Successfully", serializer.data), status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class PayrollApiIdView(APIView):
    def get_object(self, id):
        try:
            data = Payroll.objects.get(id=id)
            return data
        except Payroll.DoesNotExist:
            return None
    
    def get(self, request, id):
        instance = self.get_object(id)
        if not instance:
            return Response({"msg":"Not Found"}, status=status.HTTP_404_NOT_FOUND)
        serializer= PayrollSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, id):
        instance = self.get_object(id)
        if not instance:
            return Response({"msg":"Not Found"}, status=status.HTTP_404_NOT_FOUND)
        
        salary1 = request.POST.get('salary')
        bonus1 = request.POST.get('bonus')
        taxes1 = request.POST.get('taxes')
        other_deduction1 = request.POST.get('other_deduction')

        salary = float(salary1)
        bonus = float(bonus1)
        taxes = float(taxes1)
        other_deduction = float(other_deduction1)
        net_salary = (salary+bonus)-(taxes+other_deduction)

        data = {
            "employee" : request.POST.get('employee'),
            "pay_period_start" : request.POST.get('pay_period_start'),
            "pay_period_end" : request.POST.get('pay_period_end'),
            "salary" : salary1,
            "bonus" : bonus1,
            "taxes" : taxes1,
            "other_deduction" : other_deduction1,
            "net_salary" : net_salary
        }
        serializer = PayrollSerializer(data=data, instance=instance)
        if serializer.is_valid():
            serializer.save()
            return Response(CustomResponse.successResponse(200, "Added Successfully", serializer.data), status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, id):
        instance = self.get_object(id)
        if not instance:
            return Response({"msg":"Not Found"}, status=status.HTTP_400_BAD_REQUEST)
        instance.delete()
        return Response({"msg":"Deleted Successfully"}, status=status.HTTP_200_OK)
    
class PayrollApiPdfView(APIView):
    def get_object(self, id):
        try:
            data = Payroll.objects.filter(employee=id)
            return data
        except Payroll.DoesNotExist:
            return None

    def get(self, request, id):
        instance = self.get_object(id)
        if not instance:
            return Response({"msg":"Not Found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            data = HttpResponse(content_type='application/pdf')
            data['Content-Disposition'] = 'attatchment; filename="payroll.pdf"'

            
            pdf = canvas.Canvas(data)
            y=750
            for obj in instance:
                pdf.drawString(50, y, str(obj.employee))
                pdf.drawString(155, y, str(obj.salary))
                pdf.drawString(210, y, str(obj.bonus))
                pdf.drawString(265, y, str(obj.taxes))
                pdf.drawString(315, y, str(obj.other_deduction))
                pdf.drawString(365, y, str(obj.net_salary))
                pdf.drawString(420, y, str(obj.pay_period_start))
                pdf.drawString(500, y, str(obj.pay_period_end))
                y -= 20
            pdf.showPage()
            pdf.save()
            return data

class AttendanceApiPdfView(APIView):
    def get_object(self, id):
        try:
            data = Attendance.objects.filter(employee=id)
            return data
        except Attendance.DoesNotExist:
            return None
        
    def get(self, request, id):
        instance = self.get_object(id)
        if not instance:
            return Response({"msg":"Not Found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="attendance.pdf"'

            # Create a PDF
            pdf = canvas.Canvas(response)
            y = 750 # The y-coordinate of the first row
            for obj in instance:
                # Write each object's data to the PDF
                pdf.drawString(100, y, str(obj.employee))
                pdf.drawString(220, y, str(obj.date))
                pdf.drawString(320, y, str(obj.time_in))
                pdf.drawString(400, y, str(obj.time_out))
                pdf.drawString(490, y, str(obj.hours_worked))
                y -= 20 # Move down to the next row
            pdf.showPage()
            pdf.save()

            return response

class PayrollApiSearch(APIView):
    def get_object(self, id):
        try:
            data = Payroll.objects.filter(employee=id)
            return data
        except Payroll.DoesNotExist:
            return None
        
    def get(self, request, id):
        instance = self.get_object(id)
        if not instance:
            return Response({"msg":"Not Found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = PayrollSerializer(instance, many=True)
            return Response(CustomResponse.successResponse(200, "Payroll Lists", serializer.data), status=status.HTTP_200_OK)

class AttendanceApiSearch(APIView):
    def get_object(self, id):
        try:
            data = Attendance.objects.filter(employee=id)
            return data
        except Attendance.DoesNotExist:
            return None
        
    def get(self, request, id):
        instance = self.get_object(id)
        if not instance:
            return Response({"msg":"Not Found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = AttendanceSerializer(instance, many=True)
            return Response(CustomResponse.successResponse(200, "Attendance List", serializer.data), status=status.HTTP_200_OK)

class UserLoginApiView(APIView):
    def post(self, request):
        username = request.data.get('username', None)
        password = request.data.get('password', None)
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return Response({"Message":"You have logged in successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"error":"Username or Password doesnot match!!"}, status=status.HTTP_400_BAD_REQUEST)
        

class UserLogoutApiView(APIView):
    def get(self, request):
        user = request
        logout(user)
        return Response({"msg":"Loggedout"}, status=status.HTTP_200_OK)
    
class UserRegisterApiView(APIView):
    def get(self, request):
        user = User.objects.all()
        serializer = UserSerializer(user, many=True)
        return Response(CustomResponse.successResponse(200, "User Lists", serializer.data), status=status.HTTP_200_OK)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            data = {
                'response': "Successfully Registered new user",
                'username': user.username,
                'email': user.email
            }
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)