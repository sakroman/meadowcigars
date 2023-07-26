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
from django.views.generic import FormView, DetailView, ListView, UpdateView

from .forms import *
from .models import Wishlist
from products.models import Product


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


class ProfileView(DetailView):
    template_name = 'users/profile.html'
    model = User
    context_object_name = 'user'


class ProfileSettingsView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'users/user_settings.html'
    form_class = ProfileSettingsForm
    success_url = reverse_lazy('user:profile-settings')

    def get_object(self, queryset=None):
        return self.request.user


class WishlistView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'users/wishlist.html'
    context_object_name = 'wishlist_items'

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


class CartView(ListView):
    model = Product
    template_name = 'users/cart.html'
