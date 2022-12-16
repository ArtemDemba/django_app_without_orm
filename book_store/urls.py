from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('', views.login),
    path('index', views.index),
    path('customer_main_page', views.customer_main_page),
    path('employee_main_page', views.employee_main_page),
    path('add_book/', views.add_book)
]