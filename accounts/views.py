from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from .models import User
import bcrypt

def get_success_url():
    return getattr(settings, 'LOGIN_REDIRECT_URL', '/')


def index(request):
    if 'user_id' in request.session:
        return redirect(get_success_url())
    return render(request, "accounts/registration.html")


def register(request):
    if request.method == "POST":
        errors = User.objects.register_validator(request.POST)
        
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value, extra_tags=key)
            return render(request, "accounts/registration.html") 
            
        raw_password = request.POST['password']
        hashed_password = bcrypt.hashpw(raw_password.encode(), bcrypt.gensalt()).decode()
        
        new_user = User.objects.create(
            first_name=request.POST['first_name'].strip(),
            last_name=request.POST['last_name'].strip(),
            email=request.POST['email'].strip(),
            birthday=request.POST['birthday'],
            password=hashed_password,
            img=request.FILES.get('image')
        )
        
        request.session['user_id'] = new_user.id
        request.session['user_name'] = f"{new_user.first_name} {new_user.last_name}"
        return redirect(get_success_url())
        
    return render(request, "accounts/registration.html")


def login(request):
    if request.method == "POST":
        user_query = User.objects.filter(email=request.POST['email'].strip())
        
        if user_query:
            user = user_query[0]
            if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
                request.session['user_id'] = user.id
                request.session['user_name'] = f"{user.first_name} {user.last_name}"
                return redirect(get_success_url())
                
        messages.error(request, "Invalid email or password combination.", extra_tags="login")
        return render(request, "accounts/registration.html")
        
    return render(request, "accounts/registration.html")


def logout(request):
    request.session.flush() 
    return redirect('accounts:index')