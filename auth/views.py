from django.shortcuts import render

# Create your views here.

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

def Login(request):
    Username = request.POST.get('username')
    Password = request.POST.get('password')

    ctr = 0

    error = ""

    user = authenticate(request, username = Username, password = Password)

    if user is not None:
        login(request , user)
        # Redirect to success page
        return render(request, 'home/index.html')

    else:
        if ctr == 0:
            ctr += 1
            return render(request, 'auth/login.html', {'error' : error})
        else:
            error = "Invalid UserName or Password"
            return render(request, 'auth/login.html', {'error' : error})


def Logout(request):
    logout(request)
    return render(request, 'home/index.html')


def Signup(request):
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    mail = request.POST.get('email')
    username = request.POST.get('username')
    key = request.POST.get('pass_key')
    password = request.POST.get('password')

    if(key == "ARTEMIS"):
        user = User.objects.create_user(username, mail, password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        user = authenticate(request, username = username, password = password)
        login(request , user)
        return render(request, 'home/index.html')
    else:
        return render(request, 'auth/signup.html')


    