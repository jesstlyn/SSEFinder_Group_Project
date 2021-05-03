from django.urls import path
from Finder import views

urlpatterns = [
    path('login/', views.Login.as_view(), name='login-page'),
    path('homePage/', views.homePage.as_view(), name='home-page'),
    path('addNewCase/', views.AddNewCase.as_view(), name='addNewCase-page'),
    path('addNewEvent/', views.AddNewEvent.as_view(),name='addNewEvent-page'),
    path('searchCaseNumber/', views.searchCaseNumber.as_view(), name='searchCaseNumber'),
    path('caseNumberDetail/', views.caseNumberDetail.as_view(), name='caseNumberDetail'),
    ]
