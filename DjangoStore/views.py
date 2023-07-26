from django.views.generic import ListView

from products.models import Product


class HomeView(ListView):
    model = Product
    template_name = 'general/home.html'
    context_object_name = 'products'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['new_products'] = Product.objects.all().order_by('-created')
        return context
