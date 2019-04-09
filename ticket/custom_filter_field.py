"""
Django filters
Copyright (c) Alex Gaynor and individual contributors.
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

 * Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.
 * Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.
 * The names of its contributors may not be used to endorse or promote products
   derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


Django
Copyright (c) Django Software Foundation and individual contributors.
All rights reserved.

Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

    1. Redistributions of source code must retain the above copyright notice,
       this list of conditions and the following disclaimer.

    2. Redistributions in binary form must reproduce the above copyright
       notice, this list of conditions and the following disclaimer in the
       documentation and/or other materials provided with the distribution.

    3. Neither the name of Django nor the names of its contributors may be used
       to endorse or promote products derived from this software without
       specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""


from datetime import datetime, time
import datetime
from django import forms
from django_filters.utils import handle_timezone
from django.utils.dateparse import parse_datetime, parse_date
from django.utils.translation import ugettext_lazy as _
from django_filters.fields import RangeField
from django_filters.filters import RangeFilter
from django_filters.widgets import DateRangeWidget


import re
from django.utils import formats
from calendar import monthrange

class BeforeDateField(forms.DateField):
    """
    custom DateField for ticket search filter field deadline-enddate
    supports date input shortcuts: year only and month.year
    appends the last day of the given date (i.e. year->31.12.year)
    """
    input_formats = ['%d.%m.%Y','%m.%Y','%Y']
    default_error_messages = {
        'invalid': _('Bitte ein valides Datum eingeben'),
    }

    def to_python(self, value):
        """
        Validate that the input can be converted to a date. Returns a Python
        datetime.date object or ValidationError if given value is not valid
        """
        # if given value is empty
        if value in self.empty_values:
            return None
        # if value is a datetime object
        if isinstance(value, datetime.datetime):
            return value.date()
        # if value is date object
        if isinstance(value, datetime.date):
            return value
        # if value is a String
        if isinstance(value, str):
            # if String is more than 10 long
            if(len(value)> 10):
                raise forms.ValidationError(
                    _('Bitte ein valides Datum eingeben'),
                    code='invalid',
                )
            # given String is MM.YYYY?
            if re.match(r'[0-9]{2}.[0-9]{4}$', value):
                if int(value[:2])<13:
                    # change value: append the correct day of given month
                    value = str(monthrange(int(value[3:]),int(value[:2]))[1]) + '.' + str(value)
                else:  raise forms.ValidationError(
                    _('Kein gültiges Enddatum.'),
                    code='invalid',
                )
            # given String is YYYY?
            if re.match(r'^[0-9]{4}$', value):
                # chnage value: append 31.12.
                value = '31.12.' + str(value)
        return super().to_python(value)

    def strptime(self, value, format):
        """
        returns the date of a given value
        before that it gets converted to given format
        """
        return datetime.datetime.strptime(value, format).date()


class DateRangeField(RangeField):
    """
    custom DateRangeField for supporting BeforeDateField
    and overrides input_formats for start-date field
    """
    widget = DateRangeWidget
    def __init__(self, *args, **kwargs):
        fields = (
            forms.DateField(input_formats=['%d.%m.%Y','%m.%Y','%Y']), BeforeDateField())
        super().__init__(fields, *args, **kwargs)

    def compress(self, data_list):
        """
        param: data_list(list)- a list of the 2 entered filter dates
        returns a slice of converted normalized timezone datetimes
        or None if not given
        """
        if data_list:
            start_date, stop_date = data_list
            if start_date:
                start_date = handle_timezone(
                    datetime.datetime.combine(start_date, time.min),
                    False
                )
            if stop_date:
                stop_date = handle_timezone(
                    datetime.datetime.combine(stop_date, time.max),
                    False
                )
            return slice(start_date, stop_date)
        return None

class DateFromToRangeFilter(RangeFilter):
    """
    specifies custom DateFromToRangeFilter for deadline filtering
    used in .filters.py
    """
    field_class = DateRangeField
