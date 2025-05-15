from django.urls import path
from . import views

urlpatterns = [
    path('', views.profile, name='profile'),
    path('order_history/<order_number>', views.order_history, name='order_history'),
    path('plan_order_history/<subscription_number>', views.plan_order_history, name='plan_order_history'),
    path('save-achievement/', views.save_achievement, name='save_achievement'),
]