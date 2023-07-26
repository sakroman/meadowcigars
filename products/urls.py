from django.urls import path
from .views import *

app_name = "products"


urlpatterns = [
    # path('', ProductListView.as_view(), name='products-list'),

    path('<slug:slug>/', ProductView.as_view(), name='product-detail'),
    path('category/<str:category>/', CategoryView.as_view(), name='category'),
]
