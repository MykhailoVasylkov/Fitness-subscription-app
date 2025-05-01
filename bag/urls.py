from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_bag, name='view_bag'),
    path('add/product/<item_id>/', views.add_to_bag, name='add_to_bag'),
    path('adjust/<item_id>/', views.adjust_bag, name='adjust_bag'),
    path('remove/<item_id>/', views.remove_from_bag, name='remove_from_bag'),
    path('add/plan/<plan_id>/', views.add_plan_to_bag, name='add_plan_to_bag'),
]