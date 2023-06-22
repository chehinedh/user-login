from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from user import settings
from django.core.mail import send_mail

# Create your views here.
def home(request):
    return render(request, 'authentication/index.html')

def signup(request):
    
    if request.method == "POST":
        # Get the post parameters
        username = request.POST['username']
        firstname = request.POST['firstname']
        lastname = request.POST['firstname']
        email = request.POST['email']
        password = request.POST['password']
        pass2 = request.POST['pass2']

        if User.objects.filter(username=username):
            messages.error(request, "Username aldready exists!")
            return redirect('home')
        
        if User.objects.filter(email=email):
            messages.error(request, "Email aldready exists!")    
            return redirect('home')
        
        if len(username) > 10:
            messages.error(request, "Username must be under 10 characters!")
            return redirect('home')
        
        if password != pass2:
            messages.error(request, "Passwords do not match!")
            return redirect('home')
        
        if not username.isalnum():
            messages.error(request, "Username should only contain letters and numbers!")
            return redirect('home')

        # Create the user
        myuser = User.objects.create_user(username, email, password)
        myuser.first_name = firstname
        myuser.last_name = lastname
        myuser.is_active = False

        myuser.save()
        messages.success(request, 'Your Account has been successfully created.')

        # welcome email

        subject = 'Welcome to Django Login!'
        message = "Hello" + myuser.first_name + "!! \n" + "Welcome to Django \n Thank you for visiting our website \n We have also sent you a conformation email, please confirm your email address in order to activate your account" 
        from_email= settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)


        return redirect('signin')

    return render(request, 'authentication/signup.html')

def signin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            firstname = user.first_name
            return render(request, "authentication/index.html", {'firstname': firstname})
        else:
            messages.error(request, 'Invalid Credentials, Please try again')
            return redirect('home')

    return render(request, 'authentication/signin.html')

   

def signout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully!")
    return redirect('home')