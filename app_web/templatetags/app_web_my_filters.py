from django import template

register = template.Library()

@register.filter(name='contains')
def contains(value, arg):
    """Custom template filter to check if 'arg' is in 'value'."""
    return arg in value
