from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers as core_serializer
import json
from django.core.serializers.json import DjangoJSONEncoder


from rest_framework.decorators import api_view
from rest_framework.renderers import JSONRenderer
from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework import generics, filters
from performance.Filters import ClientFilter

from performance.serializers import serializers, ClientSerializer, ReservationSerializer
from performance.models import Client, Reservation


def index(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render())


def empty(request):
    return JSONResponse({})


def test(request):
    return core_serializer.serialize('json', Reservation.objects.all().select_related('client'),
                                 use_natural_foreign_keys=True, use_natural_primary_keys=True)

@csrf_exempt
def client_list(request):
    clients = Client.objects.all()
    serializer = ClientSerializer(clients, many=True)
    return JSONResponse(serializer.data)


@csrf_exempt
def reservation_list(request):
    reservations = Reservation.objects.all().select_related('client')
    serializer = ReservationSerializer(reservations, many=True)
    return JSONResponse(serializer.data)


@api_view(('GET',))
def api_root(request, format=None):
    return Response({
        'clients': reverse('client-list', request=request, format=format),
        'reservations': reverse('reservation-list', request=request, format=format)
    })


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


class ClientApi(generics.ListAPIView):
    queryset = Client.objects
    serializer_class = ClientSerializer
    filter_backends = (filters.DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter)
    filter_class = ClientFilter
    search_fields = ('first_name', 'last_name', 'reservation__comment')
    ordering_fields = '__all__'

    def get_queryset(self):
        queryset = super(ClientApi, self).get_queryset()
        return queryset.prefetch_related('reservations')
        # fields = self.request.GET.get('fields')
        # fields = [s.encode('ascii') for s in fields.strip('{}').split(',')]
        # return queryset.values_list(*fields).prefetch_related('reservations')

    # def list(self, request, *args, **kwargs):
    #     queryset = self.filter_queryset(self.get_queryset())
    #     return Response(queryset)