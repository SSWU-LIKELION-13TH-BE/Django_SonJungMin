from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth import login, authenticate
from .froms import SignUpForm
from .models import CustomUser
from django.contrib.auth.hashers import make_password

def home(request):
    return render(request, 'home.html')
    
def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('user:home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form':form})

def login_view(request):
    if request.method == 'POST':
        l_username=request.POST['l_username']
        l_password=request.POST['l_password']
        user=authenticate(request, username=l_username, password=l_password)
        if user is not None:
            auth.login(request, user)
            return redirect('user:home')
        return redirect('user:login')
    else:
        return render(request, 'login.html')
        
def logout_view(request):
    if request.method=="GET":
        if request.user:
            auth.logout(request)
            return redirect('user:home')
    return redirect('user:home')

def findPWwithID_view(request):
    if request.method == "POST":
        password1=request.POST['f_pw1']
        password2=request.POST['f_pw2']
        user=CustomUser.objects.get(username=request.POST['f_username'])
        if(user is not None and user.email==request.POST['f_email'] and password1==password2):
            user.password=make_password(password1)
            user.save()
        return redirect('user:home')
    else:
        return render(request, 'findPWwithID.html')