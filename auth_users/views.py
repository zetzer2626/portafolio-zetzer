from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from core.models import Profile
from .forms import CustomUserCreationForm

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Crear perfil automáticamente
            Profile.objects.create(user=user)
            login(request, user)
            messages.success(request, 'Cuenta creada exitosamente.')
            return redirect('home')
        else:
            messages.error(request, 'Error al crear la cuenta. Por favor, verifica los datos.')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'auth_users/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Bienvenido, {user.username}!')
            return redirect('home')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
    
    return render(request, 'auth_users/login.html')

@login_required
def user_logout(request):
    logout(request)
    messages.success(request, 'Has cerrado sesión exitosamente.')
    return redirect('home')

def profile_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    return render(request, 'auth_users/profile.html')
