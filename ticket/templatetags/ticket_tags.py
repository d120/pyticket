from django.template import Library

from ticket.models import Ticket
register = Library()

import json


@register.filter(name='loadjson')
def loadjson(data):
    return json.loads(data)