__author__ = 'ggarrido'

import django_filters
from performance.models import Client
from performance.serializers import ClientSerializer
from rest_framework import generics


class ClientFilter(django_filters.FilterSet):
    reservation_number = django_filters.CharFilter(name="reservation__number")

    class Meta:
        model = Client
        fields = ['id', 'first_name', 'last_name', 'reservation_number']