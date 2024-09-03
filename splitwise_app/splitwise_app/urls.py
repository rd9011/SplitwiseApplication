"""
URL configuration for splitwise_app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path 
from splitwisemtv import views

urlpatterns = [
    path('users/', views.UserView.as_view(), name='users_list'),
    path('expenses/', views.ExpenseView.as_view(), name='expenses_list'),
    path('balances/', views.BalanceView.as_view(), name='balances_list'),
]