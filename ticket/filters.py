import django_filters
from .models import Ticket
from .custom_filter_field import DateFromToRangeFilter
from django import forms
import datetime
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

def validate_range(value):
    """
    validate method for deadline: checks if the given dates
    are instances of datetime objects and stop date is equal or after start
    param: value that is being checked - expected type slice of datetime.datetime
    return: True or ValidationError
    """
    if value:
        if isinstance(value, slice):
            if(value.start):
                if(not isinstance(value.start, datetime.datetime)):
                    raise forms.ValidationError(_("Invalides Datumsformat."))
            if(value.stop):
                if(not isinstance(value.stop, datetime.datetime)):
                    raise forms.ValidationError(_("Invalides Datumsformat."))
            if(value.start and value.stop and value.start>value.stop):
                    raise forms.ValidationError(_("Das Startdatum ist jünger als das Stopdatum."))
    return True;

class TicketFilter(django_filters.FilterSet):
    """
    filter form for filtering on search_ticket.html
    used in SearchTicketView in .views
    """
    name_text = django_filters.CharFilter(method='filter_name_text', label=_('Name und Text'), lookup_expr='icontains', max_length=256)
    deadline = DateFromToRangeFilter(validators=[validate_range], widget=django_filters.widgets.DateRangeWidget(attrs={'placeholder': 'TT.MM.JJJJ', 'title':_('Zeitraum eingrenzen: von - bis jeweils inklusive. Format: TT.MM.JJJJ oder MM.JJJJ oder JJJJ')}, ))
    assigned_user = django_filters.ModelChoiceFilter(queryset=get_user_model().objects.all(), null_label='None')
    assigned_group = django_filters.ModelChoiceFilter(queryset=Group.objects.all(), null_label='None')

    class Meta:
        model = Ticket
        fields = ['name_text', 'state', 'priority', 'assigned_user', 'assigned_group', 'accepted', 'creator_user', 'deadline']

    def filter_name_text(self, queryset, id, value):
        """
        custom filter method for 'name_text' field
        param: queryset - the current queryset
        param: id
        param: value - the given value in name_text field
        """
        return queryset.filter(name__icontains=value) | queryset.filter(text__icontains=value)
