from django.urls import path
from Finder import views

urlpatterns = [
    path('', views.Login.as_view(), name='login-page'),
    path('homePage/', views.homePage.as_view(), name='home-page'),
    path('addNewCase/', views.AddNewCase.as_view(), name='addNewCase-page'),
    path('addNewEvent/', views.AddNewEvent.as_view(),name='addNewEvent-page'),
    path('searchCaseNumber/', views.searchCaseNumber.as_view(), name='searchCaseNumber'),
    path('caseNumberDetail/', views.caseNumberDetail.as_view(), name='caseNumberDetail'),
    path('createAccount/', views.CreateAccount.as_view(), name='createAccount-page'),
    path('searchEvent/', views.SearchEvent.as_view(),name='searchEvent'),
    path('eventDetail/', views.EventDetail.as_view(), name='eventDetail'),
    ]
