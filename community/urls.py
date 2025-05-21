from django.urls import path
from . import views


urlpatterns = [
    path('', views.community, name='community'),
    path('edit/<int:pk>', views.edit_post, name='edit_post'),
    path('delete/<int:pk>', views.delete_post, name='delete_post'),
]