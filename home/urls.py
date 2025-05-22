from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='home'),
    path('terms', views.terms, name='terms'),
    path('privacy', views.privacy, name='privacy'),
    path('confirm-subscription/<uuid:token>/', views.confirm_subscription, name='confirm_subscription'),
    path('unsubscribe/<uuid:token>/', views.unsubscribe, name='unsubscribe'),
]