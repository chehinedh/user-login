from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login

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
        # Create the user
        myuser = User.objects.create_user(username, email, password)
        myuser.first_name = firstname
        myuser.last_name = lastname

        myuser.save()
        messages.success(request, 'Your Account has been successfully created.')
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
    pass