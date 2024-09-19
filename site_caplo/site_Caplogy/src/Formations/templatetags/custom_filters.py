from django import template
from datetime import time

register = template.Library()

@register.filter
def format_time(value):
    if isinstance(value, time):
        return value.strftime('%H:%M')  # Formate l'heure au format 24 heures
    return value