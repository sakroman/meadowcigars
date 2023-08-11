import json

from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView, DetailView, ListView, UpdateView, TemplateView

from .forms import *
from .models import Wishlist
from products.models import Product

from DjangoStore.mixins import BrandsInContext

from products.models import OrderItem, Order


class RegistrationView(SuccessMessageMixin, FormView):
    form_class = RegistrationForm
    success_url = reverse_lazy('home')
    success_message = 'Registration successful'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'An error occurred during registration')
        print(form.errors)
        return super().form_invalid(form)

    def render_to_response(self, context, **response_kwargs):
        return HttpResponseRedirect(self.get_success_url())


class LoginPageView(LoginView):
    success_url = reverse_lazy('home')

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid username or password.')
        print(form.errors)
        return redirect('home')

    def render_to_response(self, context, **response_kwargs):
        return HttpResponseRedirect(self.get_success_url())


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('home')


class ProfileView(BrandsInContext, DetailView):
    template_name = 'users/profile.html'
    model = User
    context_object_name = 'user'


class ProfileSettingsView(BrandsInContext, LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'users/user_settings.html'
    form_class = ProfileSettingsForm
    success_url = reverse_lazy('user:profile-settings')

    def get_object(self, queryset=None):
        return self.request.user


class WishlistView(LoginRequiredMixin, BrandsInContext, ListView):
    model = Product
    template_name = 'users/wishlist.html'
    context_object_name = 'wishlist_items'
    login_url = '../profile/1'

    def get_queryset(self):
        wishlist, _ = Wishlist.objects.get_or_create(user=self.request.user)
        products = wishlist.products.all()
        return products


class AddToWishlistView(View):
    def post(self, request, *args, **kwargs):
        added = False
        product_id = json.loads(request.body)

        product = get_object_or_404(Product, id=product_id)
        wishlist, created = Wishlist.objects.get_or_create(user=request.user)
        if product not in wishlist.products.all():
            wishlist.products.add(product)
            added = True
        else:
            wishlist.products.remove(product)

        return JsonResponse({'added': added})


class RemoveFromWishlistView(View):
    def post(self, request, *args, **kwargs):
        added = True
        data = json.loads(request.body)
        product_id = data.get('product_id')

        product = get_object_or_404(Product, id=product_id)
        wishlist, created = Wishlist.objects.get_or_create(user=request.user)
        if product in wishlist.products.all():
            wishlist.products.remove(product)
            added = False
        else:
            JsonResponse

        return JsonResponse({'added': added})


def get_cart(request):
    cart_pk = request.session.get('cart')
    if cart_pk:
        cart = Order.objects.get(pk=cart_pk)
    else:

        if request.user.is_authenticated:
            cart, _ = Order.objects.get_or_create(
                user=request.user,
                status='cart'
            )
        else:
            cart = Order.objects.create(status='cart')
        request.session['cart'] = cart.pk

    return cart


class CartView(BrandsInContext, ListView):
    model = Product
    template_name = 'users/cart.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['cart'] = get_cart(self.request)
        return context


class AddToCartView(View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        product_id = data.get('product_id')
        quantity = data.get('quantity')

        if not product_id:
            return JsonResponse({'error': 'Product ID is required.'}, status=400)

        product = get_object_or_404(Product, id=product_id)

        cart = get_cart(request)

        product_order_item = cart.items.filter(product=product).first()
        if product_order_item:
            product_order_item.quantity = product_order_item.quantity + int(quantity)
            product_order_item.save()
        else:
            OrderItem.objects.create(
                order=cart,
                product=product,
                quantity=quantity
            )

        return JsonResponse({'added': True})


class RemoveFromCartView(View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        product_id = data.get('product_id')
        if product_id:

            cart = get_cart(request)
            try:
                product = Product.objects.get(pk=product_id)
                cart.items.filter(product=product).delete()
                return JsonResponse({"message": "Product removed from cart."})
            except Product.DoesNotExist:
                return JsonResponse({"error": "Product not found."}, status=400)

        else:
            return JsonResponse({"error": "Invalid product ID."}, status=400)


class CheckoutView(FormView):
    template_name = 'users/checkout.html'
    form_class = ShippingInfoForm
    success_url = 'checkout/success'

    def form_valid(self, form):
        cart = get_cart(self.request)
        if not cart.status == 'confirmed':
            cart.status = 'confirmed'
            cart.save()

        shipping_info = form.save(commit=False)
        shipping_info.order = cart
        shipping_info.save()

        self.request.session.pop('cart', None)

        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid inputs')
        print(form.errors.as_text)
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['cart'] = get_cart(self.request)
        return context


class SuccessOrder(TemplateView):
    template_name = 'users/order_success.html'


class OrdersView(ListView):
    model = Order
    template_name = 'users/orders.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['orders'] = Order.objects.filter(user=self.request.user, status='confirmed')
        return context
