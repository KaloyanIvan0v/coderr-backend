import django_filters
from django.db.models import Min
from rest_framework.exceptions import ValidationError
from core_app.models import Offer


class OfferFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(method='filter_min_price')
    max_delivery_time = django_filters.NumberFilter(
        method='filter_max_delivery_time')
    creator_id = django_filters.NumberFilter(field_name='user__id')

    class Meta:
        model = Offer
        fields = ['creator_id']

    def filter_min_price(self, queryset, name, value):
        if value < 0:
            raise ValidationError({'min_price': 'Darf nicht negativ sein'})
        return queryset.annotate(min_price=Min('details__price')).filter(min_price__gte=value)

    def filter_max_delivery_time(self, queryset, name, value):
        if value < 0:
            raise ValidationError(
                {'max_delivery_time': 'Darf nicht negativ sein'})
        return queryset.annotate(min_delivery_time_calc=Min('details__delivery_time_in_days')).filter(min_delivery_time_calc__lte=value)
