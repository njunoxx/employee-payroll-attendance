from django.urls import path
from .views import AddEmployee, EditEmployee, EditPayroll, AddPayroll, AddAttendance, EditAttendance
from .import views

urlpatterns = [
    #URL for Employee Model
    path('index/', views.index, name="employee-index"),
    path('empprofile/<int:id>/', views.employee_profile, name="employee-profile"),
    path('empadd/', AddEmployee.as_view(), name="employee-add"),
    path('empdelete/<int:id>/', views.employee_delete, name="employee-delete"),
    path('empedit/<int:id>', EditEmployee.as_view(), name="employee-edit" ),

    #URL for Payroll Model
    path('payindex/', views.payroll_index, name="payroll-index"),
    path('payprofile/', views.payroll_profile, name="payroll-profile"),
    path('payedit/<int:id>/', EditPayroll.as_view() , name="payroll-edit"),
    path('payadd/', AddPayroll.as_view(), name="payroll-add"),
    path('paydelete/', views.payroll_delete, name="payroll-delete"),

    #URL for Attendance Model
    path('attindex/', views.attendance_index, name="attendance-index"),
    path('attprofile/', views.attendance_profile, name="attendance-profile"),
    path('attadd/', AddAttendance.as_view(), name="attendance-add"),
    path('attedit/<int:id>/', EditAttendance.as_view(), name="attendance-edit"),
    path('attdelete/<int:id>/', views.attendance_delete, name='attendance-delete'),

    # URL for search method
    path('employeesearch/', views.employee_search, name="employee-search"),
    path('searchattendance/<str:name>/', views.search_attendance, name="search-attendance"),
    path('searchpayroll/<str:name>/', views.search_payroll, name='search-payroll' ),
 #path('filterview/', views.filter_view, name="filter-view"),

    # URL for PDF
    path('employeeattendancepdf/<str:name>/', views.attendance_pdf, name='attendance-pdf'),
    path('employeepayrollpdf/<str:name>/', views.payroll_pdf, name="payroll-pdf"),

]