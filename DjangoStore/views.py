from django.shortcuts import render
from django.views import View
from django.views.generic import ListView
from products.models import Product
from DjangoStore.mixins import BrandsInContext


class HomeView(BrandsInContext, ListView):
    model = Product
    template_name = 'general/home.html'
    context_object_name = 'products'

    def get_context_data(self, *args, object_list=None, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['new_products'] = Product.objects.all().order_by('-created')
        return context


class Custom404View(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'general/404.html', status=404)
