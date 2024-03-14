from django import template
from sqids import Sqids
sq = Sqids()

register = template.Library()

@register.filter
def subtract(value, arg):
    return value - arg

@register.filter
def encode_id(id):
    return sq.encode([id])