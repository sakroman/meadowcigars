from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import DetailView, ListView
from .models import Product, Field
from django.contrib import messages

from users.models import Wishlist

from DjangoStore.mixins import BrandsInContext


class ProductView(BrandsInContext, DetailView):
    template_name = 'products/product_details.html'
    model = Product
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()

        if self.request.user.is_authenticated:

            wishlist, _ = Wishlist.objects.get_or_create(user=self.request.user)
            product = context['product']
            context['is_wishlisted'] = product in wishlist.products.all()
        else:

            context['is_wishlisted'] = False

        return context


class ProductListView(BrandsInContext, ListView):
    model = Product
    template_name = 'products/products_list.html'
    context_object_name = 'products'

    def get_ordering(self):
        ordering = self.request.GET.get('order', 'name')
        direction = self.request.GET.get('dir', 'asc')

        valid_ordering = ['name', 'price']
        if ordering not in valid_ordering:
            ordering = 'name'

        direction = '' if direction == 'asc' else '-'

        return f"{direction}{ordering}"

    def get_queryset(self):
        queryset = super().get_queryset()

        get_copy = self.request.GET.copy()

        order = get_copy.pop('order', None)
        direction = get_copy.pop('dir', None)

        q = get_copy.pop('q', None)
        if q:
            q = q[0]

            queryset = queryset.filter(name__icontains=q)

        for key, value in get_copy.items():
            queryset = queryset.filter(field__name=key, field__value=value)

        # Add back 'order' and 'dir' parameters to the copied QueryDict
        if order:
            get_copy['order'] = order
        if direction:
            get_copy['dir'] = direction

        ordering = self.get_ordering()

        return queryset.order_by(ordering)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['strengths'] = Field.objects.filter(name='Strength')
        context['regions'] = Field.objects.filter(name='Region')
        return context


class CategoryView(BrandsInContext, ListView):
    model = Product
    template_name = 'products/products_list.html'
    context_object_name = 'products'
    ordering = 'name'

    def get_ordering(self):
        ordering = self.request.GET.get('order', 'name')
        direction = self.request.GET.get('dir', 'asc')

        valid_ordering = ['name', 'price']
        if ordering not in valid_ordering:
            ordering = 'name'

        direction = '' if direction == 'asc' else '-'

        return f"{direction}{ordering}"

    def get_queryset(self):
        category = self.kwargs.get('category')
        ordering = self.get_ordering()

        field_instances = Field.objects.filter(name='category', value__iexact=category)
        product_ids = field_instances.values_list('product', flat=True)

        search_query = self.request.GET.get('q')
        if search_query:

            queryset = Product.objects.filter(
                id__in=product_ids,
                name__icontains=search_query
            ).order_by(ordering)

        else:
            queryset = Product.objects.filter(id__in=product_ids).order_by(ordering)

        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['category'] = self.kwargs.get('category')
        return context


class BrandsView(BrandsInContext, ListView):
    model = Field
    template_name = 'products/brands.html'

