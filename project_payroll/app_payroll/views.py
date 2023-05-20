from django.shortcuts import render, redirect
from django.views import View 
from .models import Employee, Payroll, Attendance
from django.contrib import messages
from datetime import datetime, date
from django.http import HttpResponse

from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from django.contrib.auth.decorators import login_required

 
# Create your views here.
# Views for Employee model
@login_required(login_url='login')
def index(request):
    employee_details = Employee.objects.all()
    context = {"data":employee_details}
    return render(request, 'employee/employee_index.html', context)
    
@login_required(login_url='login')    
def employee_profile(request, id):
    emp = Employee.objects.get(id=id)
    data2 = Employee.objects.all()
    context = {"data":emp, "data2":data2}
    return render(request, 'employee/employee_profile.html', context)

@login_required(login_url='login')
def employee_delete(request, id):
    emp = Employee.objects.get(id=id)
    emp.delete()
    messages.success(request, 'Employee deleted successfully!')
    return redirect('employee-index') 

# View for Payroll Model:
@login_required(login_url='login')
def payroll_index(request):
    pay = Employee.objects.all()
    context = {"data" : pay}
    return render(request, 'payroll/payroll_index.html', context)

@login_required(login_url='login')
def payroll_profile(request):
   if request.method == "POST":
    full_name = request.POST.get('full_name')
    pay = Payroll.objects.filter(employee__full_name=full_name)
    context = {"data":pay}
    return render(request, 'payroll/payroll_profile.html', context)

@login_required(login_url='login')
def payroll_delete(request, id):
    pay = Payroll.objects.get(id=id)
    pay.delete()
    messages.success(request, "Payroll of employee Deleted Successfully!")
    return redirect('payroll-index')

# View for Attendance model:
@login_required(login_url='login')
def attendance_index(request):
    attendance = Employee.objects.all()
    context = {"data" : attendance}
    if request.method == "POST":
        employee = request.POST.get('employee')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
    # Display data according to date
        employee_attendance = Attendance.objects.filter(date__lte=end_date, date__gte=start_date, employee__full_name=employee).order_by('date') 
        context = { "data" : employee_attendance }
        return render(request, 'attendance/attendance_profile_view.html', context)
    return render(request, 'attendance/attendance_index.html', context)   

@login_required(login_url='login')
def attendance_profile(request):
    matched_field = Attendance.objects.filter(employee=request.POST.get('employee')).order_by('date')
    context = {"data": matched_field }
    return render(request, 'attendance/attendance_profile.html', context)

@login_required(login_url='login')
def attendance_delete(request, id):
    att = Attendance.objects.get(id=id)
    att.delete()
    messages.success(request, "Attendance Successfully deleted!!")
    return redirect('attendance-index')    

    

class AddEmployee(View):
    def get(self, request):
        return render(request, 'employee/add_employee.html')

    def post(self, request):
        emp = Employee()
        emp.full_name = request.POST.get('full_name')
        emp.email = request.POST.get('email')
        emp.contact = request.POST.get('contact')
        emp.address = request.POST.get('address')
        emp.gender = request.POST.get('gender')
        emp.save()
        messages.success(request, "Employee added successfully!")
        return redirect('employee-index')
    
class EditEmployee(View):
    def get(self, request, id):
        emp = Employee.objects.get(id=id)
        context = {"data" : emp}
        return render(request, 'employee/employee_edit.html', context)

    def post(self, request, id):
        emp = Employee.objects.get(id=id)
        emp.full_name = request.POST.get('full_name')
        emp.address = request.POST.get('address')
        emp.contact = request.POST.get('contact')
        emp.email = request.POST.get('email')
        emp.gender = request.POST.get('gender')
        emp.save()
        messages.success(request, "Employee updated successfully!")
        return redirect('employee-index')
    

class EditPayroll(View):
    def get(self, request, id):
        pay = Payroll.objects.get(id=id)
        context = {"data" : pay}
        return render(request, 'payroll/payroll_edit.html', context)

    def post(self, request, id):
        pay = Payroll.objects.get(id=id)
        pay.salary = request.POST.get('salary')
        pay.bonus = request.POST.get('bonus')
        pay.taxes = request.POST.get('taxes')
        pay.other_deduction = request.POST.get('other_deduction')
        pay.pay_period_start = request.POST.get('pay_period_start')
        pay.pay_period_end = request.POST.get('pay_period_end')

        salary = pay.salary
        bonus =  pay.bonus
        taxes = pay.taxes
        other_deduction = pay.other_deduction

        salary =float(salary)
        bonus = float(bonus)
        taxes = float(taxes)
        other_deduction = float(other_deduction)
        net_salary = (salary+bonus)-(taxes+other_deduction)
        pay.net_salary = net_salary
        pay.save()
        messages.success(request, "Employee Payroll details edited successfully!")
        return redirect('payroll-index')


class AddPayroll(View):
    def get(self, request):
        pay = Employee.objects.all()
        context = {"data" : pay}
        return render(request, 'payroll/payroll_add.html', context)

    def post(self, request):
        try:
            pay_period_start = request.POST.get('pay_period_start')
            pay = Payroll()
            employee = Employee.objects.get(id=request.POST.get('employee'))
            pay.employee = employee
            pay.salary = request.POST.get('salary')
            pay.bonus = request.POST.get('bonus')
            pay.taxes = request.POST.get('taxes')
            pay.other_deduction = request.POST.get('other_deductions')
            pay.pay_period_start = request.POST.get('pay_period_start')
            pay.pay_period_end = request.POST.get('pay_period_end')

            salary = pay.salary
            bonus =  pay.bonus
            taxes = pay.taxes
            other_deduction = pay.other_deduction
            
            salary =float(salary)
            bonus = float(bonus)
            taxes = float(taxes)
            other_deduction = float(other_deduction)
            net_salary = (salary+bonus)-(taxes+other_deduction)
            pay.net_salary = net_salary
            pay.status = True if request.POST.get("status")=="status" else False
    # check User adding multiple Payroll data for same month and year
            status = Payroll.objects.filter(status=True,
                                            employee=request.POST.get('employee'),
                                            pay_period_start__year=pay_period_start[:4], 
                                            pay_period_start__month=request.POST.get('pay_period_start')[5:7]
                                            )
            if status.exists():
                messages.error(request, "Payroll for this Month has already been added!!")
                return redirect('payroll-add')
            else:
                pay.save()
                messages.success(request, "Employee Payroll details added successfully!")
                return redirect('payroll-index')
        except:
            messages.error(request, "Something Went wrong!!")
            return redirect('payroll-index')

class AddAttendance(View):
    def get(self, request):
        emp = Employee.objects.all()
        context = { "data" : emp }
        return render(request, 'attendance/attendance_add.html', context)

    def post(self, request):
        attendance_date = request.POST.get('date')
        time_in1 = request.POST.get('start_in')
        time_out1 = request.POST.get('start_out')
        time_in2 = datetime.strptime(time_in1, '%H:%M') 
        time_out2 = datetime.strptime(time_out1, '%H:%M')
        try:
     # condition that enables employee to create attendance for present date only
            if attendance_date < str(date.today()) or attendance_date > str(date.today()):
                messages.error(request, "Error!!! You have entered PAST or Future Date. Please Try again.")
                return redirect('attendance-add')
            
            elif time_in1 < "09:00" or time_in1>"09:00" and time_out1<"17:00" or time_out1>"17:00":
                messages.error(request, "You have selected invalid time frame!!")
                return redirect('attendance-add')
                
            else:
                emp = Employee.objects.get(id=request.POST.get('employee'))
                att = Attendance()
                att.employee = emp
                att.date = request.POST.get('date')
               
                time_in = time_in2
                time_out = time_out2
    # calculation of total working hours
                hours_worked = time_out - time_in
                att.time_in = time_in1
                att.time_out = time_out1
                att.hours_worked = hours_worked
                att.status = True if request.POST.get('status')=="status" else False
    # Check if User has already performed his attendance in the given date    
                status = Attendance.objects.filter(status=True,
                                                   employee=request.POST.get('employee'),
                                                   date=request.POST.get('date'))
                if status.exists():
                    messages.error(request, "You have already recorded your attendance today!!")
                    return redirect('attendance-add')
                else:
                    att.save()
                    messages.success(request, "Success!!! Attendance added successfully.")
                    return redirect('attendance-index')
        except:
            messages.error(request, "Something went wrong!")
            return redirect('attendance-index')    
        

class EditAttendance(View):
    def get(self, request, id):
        att = Attendance.objects.get(id=id)
        context = { "data": att }
        return render(request, 'attendance/attendance_edit.html', context)

    def post(self, request, id):
        att = Attendance.objects.get(id=id)
       
        att.date = request.POST.get('date')
        time_in1 = request.POST.get('time_in')
        time_out1 = request.POST.get('time_out')

        time_in = datetime.strptime(time_in1, '%H:%M')
        time_out = datetime.strptime(time_out1, '%H:%M')
        hours_worked = time_out - time_in
        att.time_in = time_in1
        att.time_out = time_out1
        att.hours_worked = hours_worked
        att.save()
        messages.success(request, "Attendance of employee Edited Successfully")
        return redirect('attendance-index')
    
# View for search 
@login_required(login_url='login')
def employee_search(request):
        searched=request.GET['search']
        if len(searched)>10:
            emp = []
        else:    
            emp = Employee.objects.filter(full_name__icontains=searched)
        context = {"data" : emp, "query" : searched}
        return render(request, 'employee/employee_search.html', context)

@login_required(login_url='login')
def search_attendance(request, name):
    profile = Attendance.objects.filter(employee__full_name=name).order_by('date')
    context = {"data" : profile}
    return render(request, 'attendance/attendance_profile_view.html', context)

@login_required(login_url='login')
def search_payroll(request, name):
    profile = Payroll.objects.filter(employee__full_name=name).order_by('pay_period_start')
    context = {"data" : profile}
    return render(request, 'payroll/payroll_profile.html', context)


# Generate PDF File:
@login_required(login_url='login')
def attendance_pdf(request, name):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="attendance.pdf"'

    # Retrieve all data from the database
    data = Attendance.objects.filter(employee__full_name=name)

    # Create a PDF
    pdf = canvas.Canvas(response)
    y = 750 # The y-coordinate of the first row
    for obj in data:
        # Write each object's data to the PDF
        pdf.drawString(100, y, str(obj.employee))
        pdf.drawString(200, y, str(obj.date))
        pdf.drawString(300, y, str(obj.time_in))
        pdf.drawString(400, y, str(obj.time_out))
        pdf.drawString(500, y, str(obj.hours_worked))
        y -= 20 # Move down to the next row
    pdf.showPage()
    pdf.save()

    return response


@login_required(login_url='login')
def payroll_pdf(request, name):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attatchment; filename="payroll.pdf"'

    data = Payroll.objects.filter(employee__full_name=name)
    pdf = canvas.Canvas(response)
    y=750
    for obj in data:
        pdf.drawString(50, y, str(obj.employee))
        pdf.drawString(150, y, str(obj.salary))
        pdf.drawString(210, y, str(obj.bonus))
        pdf.drawString(265, y, str(obj.taxes))
        pdf.drawString(320, y, str(obj.other_deduction))
        pdf.drawString(360, y, str(obj.net_salary))
        pdf.drawString(420, y, str(obj.pay_period_start))
        pdf.drawString(500, y, str(obj.pay_period_end))
        y -= 20
    pdf.showPage()
    pdf.save()
    return response