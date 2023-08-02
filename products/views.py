from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import DetailView, ListView
from .models import Product, Field, Category
from django.contrib import messages

from users.models import Wishlist

from DjangoStore.mixins import BrandsInContext


class ProductView(DetailView):
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
        ordering = self.request.GET.get('order', 'name')  # Default ordering by name
        direction = self.request.GET.get('dir', 'asc')  # Default direction is ascending

        # Ensure the ordering field is valid
        valid_ordering = ['name', 'price']
        if ordering not in valid_ordering:
            ordering = 'name'

        # If direction is not 'asc', set to '-' for descending order
        direction = '' if direction == 'asc' else '-'

        return f"{direction}{ordering}"

    def get_queryset(self):
        queryset = super().get_queryset()

        # Create a copy of the GET parameters
        get_copy = self.request.GET.copy()

        # Temporarily remove 'order' and 'dir' parameters from the copied QueryDict
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

        # Get the final ordering based on 'order' and 'dir' parameters
        ordering = self.get_ordering()

        return queryset.order_by(ordering)


class CategoryView(BrandsInContext, ListView):
    model = Product
    template_name = 'products/products_list.html'
    context_object_name = 'products'
    ordering = 'name'

    def get_ordering(self):
        ordering = self.request.GET.get('order', 'name')  # Default ordering by name
        direction = self.request.GET.get('dir', 'asc')  # Default direction is ascending

        # Ensure the ordering field is valid
        valid_ordering = ['name', 'price']
        if ordering not in valid_ordering:
            ordering = 'name'

        # If direction is not 'asc', set to '-' for descending order
        direction = '' if direction == 'asc' else '-'

        return f"{direction}{ordering}"

    def get_queryset(self):
        category = self.kwargs.get('category')
        ordering = self.get_ordering()


        # categories = Product.objects.filter(categories=)
        field_instances = Field.objects.filter(name='category', value__iexact=category)
        product_ids = field_instances.values_list('product', flat=True)

        search_query = self.request.GET.get('q')
        if search_query:
            # Redirect the user to the category view with the search query

            # Apply search filter to the queryset
            queryset = Product.objects.filter(
                id__in=product_ids,
                name__icontains=search_query  # Filter products with names containing the search query
            ).order_by(ordering)

        else:
            queryset = Product.objects.filter(id__in=product_ids).order_by(ordering)

        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['category'] = self.kwargs.get('category')
        return context

