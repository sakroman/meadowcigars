# custom_filters.py

from django import template

register = template.Library()


@register.simple_tag
def cigar_characteristics_dropdown():
    from .models import Field
    lengths = Field.objects.filter(name='Length')
    strengths = Field.objects.filter(name='Strength')

    return {'lengths': lengths, 'strengths': strengths}


@register.filter
def get_field_value(product, field_name):
    try:
        return product.field_set.get(name=field_name).value
    except product.field_set.model.DoesNotExist:
        return None


@register.simple_tag
def url_replace(request, field, value):
    """Appends a new GET url argument to the request's url.
    Returns the new GET parmeters as a URL-encoded string."""
    dict_ = request.GET.copy()
    dict_[field] = value

    return dict_.urlencode()


@register.simple_tag
def proper_order(request, field, value, dir=None):
    """Appends a new GET url argument to the request's url.
    Returns the new GET parmeters as a URL-encoded string."""
    dict_ = request.GET.copy()
    dict_[field] = value
    if dir is not None:
        dict_['dir'] = dir
    else:
        dict_.pop('dir', None)
    return dict_.urlencode()
