from django import template

register = template.Library()


# model_name template custom filter to apply in templates "|model_name"
@register.filter
def model_name(obj):
    try:
        return obj._meta.model_name
    except AttributeError:
        return None
