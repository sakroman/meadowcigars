from django.views.generic import ListView

from products.models import Product


class HomeView(ListView):
    model = Product
    template_name = 'general/home.html'
    context_object_name = 'products'
