from django.contrib.admin import filters
from django.http import HttpResponse
from django.http.response import JsonResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt

from rest_framework.decorators import api_view
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework import generics, renderers, filters
from performance.Filters import ClientFilter

from performance.serializers import serializers, ClientSerializer, ReservationSerializer, ClientHyperSerializer
from performance.models import Client, Reservation


def index(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render())


def test(request):
    return serializers.serialize('json', Reservation.objects.all().select_related('client'),
                                 use_natural_foreign_keys=True, use_natural_primary_keys=True)
    return JsonResponse(get_all_reservation(), safe=False)


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


@csrf_exempt
def client_list(request):
    clients = Client.objects.all()
    serializer = ClientHyperSerializer(clients, many=True)
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


class ClientApi(generics.ListAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientHyperSerializer
    filter_backends = (filters.DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter)
    filter_class = ClientFilter
    search_fields = ('first_name', 'last_name', 'reservation__comment')
    ordering_fields = '__all__'