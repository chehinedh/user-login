from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages

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
    return render(request, 'authentication/signin.html')

def signout(request):
    pass