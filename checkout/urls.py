from django.urls import path
from . import views
from .webhooks import webhook

urlpatterns = [
    path('', views.checkout, name='checkout'),
    path('checkout/success/order/<order_number>/', views.checkout_success, name='order_success'),
    path('checkout/success/subscription/<subscription_number>/', views.checkout_success, name='subscription_success'),
    path('cache_checkout_data/', views.cache_checkout_data, name='cache_checkout_data'),
    path('wh/', webhook, name='webhook'),
]