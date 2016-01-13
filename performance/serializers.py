__author__ = 'ggarrido'

from rest_framework import serializers
from performance.models import Client, Reservation


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """
    def get_fields(self):
        # Instantiate the superclass normally
        super_fields = super(DynamicFieldsModelSerializer, self).get_fields()

        fields = self.context['request'].GET.get('fields')
        if fields:
            for super_field in super_fields:
                if super_field not in fields:
                    super_fields.pop(super_field)
        return super_fields


class ReservationSerializer(DynamicFieldsModelSerializer, serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ('id', 'number', 'comment', 'client')


class ClientSerializer(DynamicFieldsModelSerializer, serializers.ModelSerializer):
    reservations = ReservationSerializer(many=True, read_only=True)

    class Meta:
        model = Client
        fields = ('id', 'first_name', 'last_name', 'reservations')


class ClientHyperSerializer(DynamicFieldsModelSerializer, serializers.HyperlinkedModelSerializer):
    reservations = ReservationSerializer(many=True, read_only=True)

    class Meta:
        model = Client
        fields = ('id', 'first_name', 'last_name', 'reservations')