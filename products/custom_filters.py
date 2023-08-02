# custom_filters.py

from django import template

register = template.Library()


@register.filter
def get_field_value(product, field_name):
    try:
        return product.field_set.get(name=field_name).value
    except product.field_set.model.DoesNotExist:
        return None
