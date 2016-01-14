from django.conf.urls import include, url
from django.contrib import admin
from performance import views
from performance.datatables import OrderListJson


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.index, name='home'),
    url(r'^empty$', views.empty, name='empty'),
    url(r'^test$', views.test, name='test'),
    url(r'^table$', OrderListJson.as_view(), name='order_list_json'),

    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    url(r'^api$', views.api_root),
    url(r'^api/clients$', views.ClientApi.as_view()),
    url(r'^api/clients/list$', views.client_list),
    url(r'^api/reservations/list$', views.reservation_list),
]
