from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import Profile
# from django.http import HttpResponse


# Create your views here.
def index(request):
    return render(request, 'index.html')


def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, "Invalid username or password")
            return redirect('signin')

    else:
        return render(request, 'signin.html')


def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm = request.POST['confirm']

        if password == confirm:
            if User.objects.filter(email=email).exists():
                messages.info(request, "Email Token")
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, "UserName Token")
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()

                # Log user in and redirect to settings page

                # create a Profile object for the new user
                user_model = User.objects.get(username=username)
                user_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                user_profile.save()
                return redirect('signin')

        else:
            messages.info(request, 'Password not matching')
            return redirect('signup')

    else:
        return render(request, 'signup.html')