from django.urls import path
from . import views

urlpatterns = [
    path('', views.customer_form, name='customer_form'),
    path('list/', views.customer_list, name='customer_list'),
    path('edit/<int:pk>/', views.customer_edit, name='customer_edit'),
    path('delete/<int:pk>/', views.customer_delete, name='customer_delete'),
]