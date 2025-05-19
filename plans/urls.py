from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_plans, name='plans'),
    path('<int:plan_id>/', views.plan_detail, name='plan_detail'),
    path('<int:plan_id>/review_create/', views.review_create, name='review_create'),
]