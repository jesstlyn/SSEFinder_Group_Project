from django.urls import path
from Finder import views

urlpatterns = [
    path('homePage/', views.homePage.as_view(), name='home-page'),
    path('loginForm/', views.Login.as_view(), name='login-page'),
    path('addNewCase/', views.AddNewCase.as_view(), name='addNewCase-page'),
    path('addNewEvent/', views.AddNewEvent.as_view(),name='addNewEvent-page'),
    ]
