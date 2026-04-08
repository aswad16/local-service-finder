from django.shortcuts import render
from django.db.models import Q, Avg, Count
from services.models import Service, Category
import anthropic
from django.conf import settings
import json


def get_ai_suggestions(query, results_count, categories):
    """Get Claude AI suggestions for the search query."""
    if not settings.ANTHROPIC_API_KEY:
        return None
    try:
        client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
        category_names = ', '.join([c.name for c in categories])
        message = client.messages.create(
            model="claude-opus-4-5",
            max_tokens=300,
            messages=[
                {
                    "role": "user",
                    "content": (
                        f"A user searched for '{query}' on a local services marketplace. "
                        f"We found {results_count} results. Available categories: {category_names}. "
                        f"Give 2-3 short, helpful tips (each max 15 words) to help them find what they need. "
                        f"Respond ONLY with a JSON array of strings. Example: [\"tip one\", \"tip two\"]"
                    )
                }
            ]
        )
        raw = message.content[0].text.strip()
        # Strip markdown fences if present
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        return json.loads(raw.strip())
    except Exception:
        return None


def search_view(request):
    query = request.GET.get('q', '').strip()
    city = request.GET.get('city', '').strip()
    category_slug = request.GET.get('category', '').strip()
    min_price = request.GET.get('min_price', '').strip()
    max_price = request.GET.get('max_price', '').strip()
    sort_by = request.GET.get('sort', 'recent')

    services = Service.objects.filter(is_active=True).select_related('provider', 'category')

    if query:
        services = services.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(category__name__icontains=query) |
            Q(provider__username__icontains=query) |
            Q(city__icontains=query)
        )
    if city:
        services = services.filter(city__icontains=city)
    if category_slug:
        services = services.filter(category__slug=category_slug)
    if min_price:
        try:
            services = services.filter(price__gte=float(min_price))
        except ValueError:
            pass
    if max_price:
        try:
            services = services.filter(price__lte=float(max_price))
        except ValueError:
            pass

    if sort_by == 'price_asc':
        services = services.order_by('price')
    elif sort_by == 'price_desc':
        services = services.order_by('-price')
    elif sort_by == 'rating':
        services = services.annotate(avg_r=Avg('reviews__rating')).order_by('-avg_r')
    elif sort_by == 'popular':
        services = services.order_by('-views_count')
    else:
        services = services.order_by('-created_at')

    categories = Category.objects.all()
    results_count = services.count()

    ai_suggestions = None
    if query and results_count >= 0:
        ai_suggestions = get_ai_suggestions(query, results_count, categories)

    return render(request, 'search/search_results.html', {
        'services': services,
        'query': query,
        'city': city,
        'category_slug': category_slug,
        'min_price': min_price,
        'max_price': max_price,
        'sort_by': sort_by,
        'categories': categories,
        'results_count': results_count,
        'ai_suggestions': ai_suggestions,
    })


def ai_recommend_view(request):
    """AI-powered service recommendations page."""
    user_need = request.GET.get('need', '').strip()
    recommendations = None
    services = []

    if user_need and settings.ANTHROPIC_API_KEY:
        try:
            client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
            all_services = Service.objects.filter(is_active=True).values(
                'title', 'category__name', 'city', 'price', 'price_type'
            )[:50]
            service_list = json.dumps(list(all_services), default=str)

            message = client.messages.create(
                model="claude-opus-4-5",
                max_tokens=500,
                messages=[
                    {
                        "role": "user",
                        "content": (
                            f"User needs: '{user_need}'. "
                            f"Available services: {service_list}. "
                            f"Recommend the top 3 most relevant service titles from the list. "
                            f"Respond ONLY with a JSON array of title strings. "
                            f"Example: [\"title1\", \"title2\", \"title3\"]"
                        )
                    }
                ]
            )
            raw = message.content[0].text.strip()
            if raw.startswith("```"):
                raw = raw.split("```")[1]
                if raw.startswith("json"):
                    raw = raw[4:]
            recommended_titles = json.loads(raw.strip())
            services = Service.objects.filter(
                title__in=recommended_titles, is_active=True
            ).select_related('provider', 'category')
            recommendations = recommended_titles
        except Exception as e:
            recommendations = []

    return render(request, 'search/ai_recommend.html', {
        'user_need': user_need,
        'recommendations': recommendations,
        'services': services,
    })
