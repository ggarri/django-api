__author__ = 'ggarrido'

from django_datatables_view.base_datatable_view import BaseDatatableView
from performance.models import Reservation


class OrderListJson(BaseDatatableView):
    # The model we're going to show
    model = Reservation
    columns = ['id', 'number', 'comment', 'client']
    order_columns = ['id', 'number', 'comment', 'client']
    max_display_length = 500

    def render_column(self, row, column):
        # We want to render user as a custom column
        if column == 'client':
            return '{0} {1}'.format(row.client.first_name, row.client.last_name)
        else:
            return super(OrderListJson, self).render_column(row, column)

    def filter_queryset(self, qs):
        # use parameters passed in GET request to filter queryset

        # simple example:
        search = self.request.GET.get(u'search[value]', None)
        if search:
            qs = qs.filter(id__istartswith=search)
        return qs