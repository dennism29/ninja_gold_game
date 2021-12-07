from django.urls import path, include
from . import views

urlpatterns = [
    path('play/', views.index),
    path('process_money/', views.process_money),
    path('reset/', views.reset),
    path('', views.set_limit)
]