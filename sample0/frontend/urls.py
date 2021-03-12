from django.urls import path
from . import  views

urlpatterns = [
    path('', views.index, name="index"),
    path('about/', views.about, name='about'),
    path('industries/', views.industries, name='industries'),
    path('contact/', views.contact, name='contact'),
    path('widget/', views.widget, name='widget'),
]