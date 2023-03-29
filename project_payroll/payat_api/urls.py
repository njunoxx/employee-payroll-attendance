from django.urls import path
from .views import EmployeeApiView, EmployeeApiIdView, AttendanceApiView, AttendanceApiIdView, PayrollApiView, PayrollApiIdView, PayrollApiPdfView, AttendanceApiPdfView, PayrollApiSearch, AttendanceApiSearch, UserLoginApiView, UserLogoutApiView, UserRegisterApiView

urlpatterns = [
    path('employee/', EmployeeApiView.as_view()),
    path('employee/<int:id>/', EmployeeApiIdView.as_view()),
    path('attendance/', AttendanceApiView.as_view()),
    path('attendance/<int:id>/', AttendanceApiIdView.as_view()),
    path('payroll/', PayrollApiView.as_view()),
    path('payroll/<int:id>/', PayrollApiIdView.as_view()),
    path('payrollpdf/<int:id>/', PayrollApiPdfView.as_view()),
    path('attendancepdf/<int:id>/', AttendanceApiPdfView.as_view()),
    path('payrollsearch/<int:id>/', PayrollApiSearch.as_view()),
    path('attendancesearch/<int:id>/', AttendanceApiSearch.as_view()),
    path('authentication/login/', UserLoginApiView.as_view()),
    path('authentication/logout/', UserLogoutApiView.as_view()),
    path('authentication/register/', UserRegisterApiView.as_view()),
]