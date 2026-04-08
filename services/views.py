from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Avg, Count, Q
from .models import Service, Category
from .forms import ServiceForm
from reviews.models import Review


def home_view(request):
    featured = Service.objects.filter(is_active=True, is_featured=True).select_related('provider', 'category')[:6]
    recent = Service.objects.filter(is_active=True).select_related('provider', 'category')[:8]
    categories = Category.objects.annotate(count=Count('services')).order_by('-count')[:8]
    stats = {
        'providers': Service.objects.values('provider').distinct().count(),
        'services': Service.objects.filter(is_active=True).count(),
        'categories': Category.objects.count(),
        'reviews': Review.objects.count(),
    }
    return render(request, 'home.html', {
        'featured': featured,
        'recent': recent,
        'categories': categories,
        'stats': stats,
    })


def service_list_view(request):
    services = Service.objects.filter(is_active=True).select_related('provider', 'category')
    category_slug = request.GET.get('category')
    city = request.GET.get('city')
    if category_slug:
        services = services.filter(category__slug=category_slug)
    if city:
        services = services.filter(city__icontains=city)
    categories = Category.objects.all()
    return render(request, 'services/service_list.html', {
        'services': services,
        'categories': categories,
        'selected_category': category_slug,
    })


def service_detail_view(request, slug):
    service = get_object_or_404(Service, slug=slug, is_active=True)
    service.views_count += 1
    service.save(update_fields=['views_count'])
    reviews = service.reviews.select_related('reviewer').order_by('-created_at')
    related = Service.objects.filter(
        category=service.category, is_active=True
    ).exclude(pk=service.pk)[:4]
    user_review = None
    if request.user.is_authenticated:
        user_review = reviews.filter(reviewer=request.user).first()
    return render(request, 'services/service_detail.html', {
        'service': service,
        'reviews': reviews,
        'related': related,
        'user_review': user_review,
    })


@login_required
def provider_dashboard_view(request):
    if not request.user.is_provider:
        messages.error(request, 'Access denied. Provider account required.')
        return redirect('home')
    services = Service.objects.filter(provider=request.user).annotate(
        avg_r=Avg('reviews__rating'),
        review_cnt=Count('reviews')
    ).order_by('-created_at')
    stats = {
        'total': services.count(),
        'active': services.filter(is_active=True).count(),
        'total_views': sum(s.views_count for s in services),
        'total_reviews': sum(s.review_cnt or 0 for s in services),
    }
    return render(request, 'services/provider_dashboard.html', {
        'services': services,
        'stats': stats,
    })


@login_required
def service_create_view(request):
    if not request.user.is_provider:
        messages.error(request, 'Only providers can create services.')
        return redirect('home')
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES)
        if form.is_valid():
            service = form.save(commit=False)
            service.provider = request.user
            service.save()
            messages.success(request, 'Service created successfully!')
            return redirect('services:provider_dashboard')
    else:
        form = ServiceForm()
    return render(request, 'services/service_form.html', {'form': form, 'action': 'Create'})


@login_required
def service_edit_view(request, slug):
    service = get_object_or_404(Service, slug=slug, provider=request.user)
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES, instance=service)
        if form.is_valid():
            form.save()
            messages.success(request, 'Service updated successfully!')
            return redirect('services:provider_dashboard')
    else:
        form = ServiceForm(instance=service)
    return render(request, 'services/service_form.html', {'form': form, 'action': 'Edit', 'service': service})


@login_required
def service_delete_view(request, slug):
    service = get_object_or_404(Service, slug=slug, provider=request.user)
    if request.method == 'POST':
        service.delete()
        messages.success(request, 'Service deleted.')
        return redirect('services:provider_dashboard')
    return render(request, 'services/service_confirm_delete.html', {'service': service})
