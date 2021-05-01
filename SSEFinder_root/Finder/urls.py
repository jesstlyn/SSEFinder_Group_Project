from django.urls import path
from Finder import views

urlpatterns = [
    path('homePage/', views.homePage.as_view(), name='home-page'),
    path('login/', views.Login.as_view(), name='login-page'),
    path('searchCaseNumber/', views.searchCaseNumber.as_view(), name='searchCaseNumber'),
    path('caseNumberDetail/', views.caseNumberDetail.as_view(), name='caseNumberDetail')
    ]
