from django.urls import path
from .views import *

app_name = "user"

urlpatterns = [
    path('login/', LoginPageView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('profile/<int:pk>/', ProfileView.as_view(), name='profile'),
    path('profile/settings/', ProfileSettingsView.as_view(), name='profile-settings'),
    path('wishlist/', WishlistView.as_view(), name='wishlist'),
    path('wishlist/add/', AddToWishlistView.as_view(), name='add_to_wishlist'),
    path('cart', CartView.as_view(), name='cart'),
    path('cart/add/', AddToCartView.as_view(), name='add_to_cart'),
    path('orders', OrdersView.as_view(), name='orders'),
    path('checkout', CheckoutView.as_view(), name='checkout'),
    path('checkout/success', SuccessOrder.as_view(), name='success'),

]
