from django.urls import path
from Finder import views

urlpatterns = [
    path('homePage/', views.homePage.as_view(), name='home-page'),
    path('login/', views.LoginPage.as_view(), name='login-page')
    ]
