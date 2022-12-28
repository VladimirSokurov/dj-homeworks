from django_filters import rest_framework as filters1
from rest_framework.viewsets import ModelViewSet
from rest_framework import filters

from logistic.models import Product, Stock
from logistic.serializers import ProductSerializer, StockSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', ]


class StockViewSet(ModelViewSet):
    serializer_class = StockSerializer
    queryset = Stock.objects.all()
    filter_backends = [filters.SearchFilter, filters1.DjangoFilterBackend]
    filterset_fields = ['products']
    search_fields = ['products__title']
