from django import template

register = template.Library()

@register.filter
def check_mp4(value):
    if (value.endswith('.mp4')):
        return True
    else:
        return False
    
