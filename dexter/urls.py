from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('inventions', views.inventions, name='inventions'),
    path('inventions/<int:id>', views.verify, name='verify'),
    path('accounts/login', views.login, name='login'),
    path('accounts/logout', views.logout, name='logout'),
    path('accounts/register', views.register, name='register'),
    path('account', views.account, name='account'),
    path('account/remove/<int:id>', views.remove, name='remove'),
    path('account/edit', views.edit, name='edit'),
    path('account/change-password', views.change_pass, name='change-password'),
    path('contact', views.contact, name='contact'),
]
