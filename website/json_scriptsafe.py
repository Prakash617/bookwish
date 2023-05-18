from django import template
from django_json import json_script

register = template.Library()

@register.filter(name='json_scriptsafe')
def json_scriptsafe(value):
    return json_script(value, safe=True)
