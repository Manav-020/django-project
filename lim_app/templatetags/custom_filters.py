from django import template
from decimal import Decimal

register = template.Library()

@register.filter
def multiply(value, arg):
    try:
        if isinstance(value, Decimal):
            return value * Decimal(str(arg))
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0

from django import template
from decimal import Decimal

register = template.Library()

@register.filter
def multiply(value, arg):
    try:
        if isinstance(value, Decimal):
            return value * Decimal(str(arg))
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0

