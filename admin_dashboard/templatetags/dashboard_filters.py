from django import template
from print_service.models import PrintOrder
from typing_service.models import TypingOrder

register = template.Library()

@register.filter
def get_order_type(order):
    if isinstance(order, PrintOrder):
        return 'print'
    elif isinstance(order, TypingOrder):
        return 'typing'
    return ''

@register.filter
def endswith(value, arg):
    return str(value).endswith(arg)