from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from django.contrib import messages

def loginPanel(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None and user.is_superuser:
            login(request, user )
            return redirect('schema-swagger-ui')
        else:
            messages.info(request, " username or passowrd is incorrect")

    return render(request, 'login.html', {})

@login_required(login_url="loginPanel")
def index(request):
    return redirect('schema-swagger-ui')

@login_required(login_url="loginPanel")
def logoutManager(request):
    logout(request)
    return redirect('loginPanel')

@login_required(login_url="loginPanel")
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Importante
            messages.success(
                request, 'Your password was successfully updated!')
            return redirect('change_passwordManager')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    
    return render(request, 'reset_password.html', {
        'form': form
    })
