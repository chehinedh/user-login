from email.message import EmailMessage
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from user import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.encoding import smart_str as force_text
from .tokens import generate_token

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


        # Email Address Confirmation Email

        current_site = get_current_site(request)
        email_subject = 'Activate your account'
        message2 = render_to_string('email_conformation.html',{
            'name': myuser.first_name,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
            'token': generate_token.make_token(myuser),
        })

        email = EmailMessage(
            email_subject,
            message2,
            settings.EMAIL_HOST_USER,
            [myuser.email],
        )

        email.fail_silently = True
        email.send()

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

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        myuser = None

    if myuser is not None and generate_token.check_token(myuser, token):
        myuser.is_active = True
        myuser.save()
        login(request, myuser)
        return redirect('home')
    else:
        return render(request, 'activation_failed.html')
