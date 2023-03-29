from django.shortcuts import render, redirect
from django.views import View
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login, logout

# Create your views here.
class UserLogin(View):
    def get(self, request):
        return render(request, 'authentication/login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, "You have logged in Successfully!!")
            return redirect('employee-index')
        else:
            messages.error(request, "Username or password doesnot match. Please try again!!!")
            return redirect('login')
        

class UserLogout(View):
    def get(self, request):
        user = request
        logout(user)
        messages.success(request, "You have logged out successfully!")
        return redirect('login')
