from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from .models import Service, Category
from .serializers import ServiceSerializer, CategorySerializer


class ServiceListCreateAPIView(generics.ListCreateAPIView):
    queryset = Service.objects.filter(is_active=True).select_related('provider', 'category')
    serializer_class = ServiceSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category__slug', 'city', 'price_type', 'is_featured']
    search_fields = ['title', 'description', 'city']
    ordering_fields = ['price', 'created_at', 'views_count']


class ServiceDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'


class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
