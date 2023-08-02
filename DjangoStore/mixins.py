from products.models import Field


class BrandsInContext:
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['brands'] = Field.objects.filter(name='Brands').values_list('value', flat=True).distinct()
        return context
