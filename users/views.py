from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import DetailView
from .forms import RegisterForm, LoginForm, ProfileUpdateForm
from .models import CustomUser
from services.models import Service
from reviews.models import Review


def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome, {user.username}! Account created successfully.')
            if user.is_provider:
                return redirect('services:provider_dashboard')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = RegisterForm()

    return render(request, 'users/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            next_url = request.GET.get('next', '')
            if next_url:
                return redirect(next_url)
            if user.is_admin_user:
                return redirect('adminpanel:dashboard')
            if user.is_provider:
                return redirect('services:provider_dashboard')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()

    return render(request, 'users/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('home')


@login_required
def profile_view(request):
    user = request.user
    services = Service.objects.filter(provider=user) if user.is_provider else None
    reviews = Review.objects.filter(reviewer=user).order_by('-created_at')[:5]

    return render(request, 'users/profile.html', {
        'profile_user': user,
        'services': services,
        'reviews': reviews,
    })


@login_required
def profile_edit_view(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('users:profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ProfileUpdateForm(instance=request.user)

    return render(request, 'users/profile_edit.html', {'form': form})


def provider_detail_view(request, pk):
    provider = get_object_or_404(CustomUser, pk=pk, role='provider')
    services = Service.objects.filter(provider=provider, is_active=True)
    reviews = Review.objects.filter(service__provider=provider).order_by('-created_at')[:10]
    avg_rating = provider.service_set.filter(is_active=True).aggregate(
        avg=__import__('django.db.models', fromlist=['Avg']).Avg('reviews__rating')
    )

    return render(request, 'users/provider_detail.html', {
        'provider': provider,
        'services': services,
        'reviews': reviews,
    })
