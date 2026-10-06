from django_filters.rest_framework import FilterSet, NumberFilter
from .models import Product


class ProductFilter(FilterSet):
    collection_id = NumberFilter(field_name='Collection_id')
    class Meta:
        model=Product
        fields={'Collection_id':['exact'],
                'unit_price':['gt','lt']
        }