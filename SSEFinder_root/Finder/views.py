from django.shortcuts import render
from django.views.generic import TemplateView, View
from django.contrib import messages

class homePage(TemplateView):
    template_name = 'homePage.html'


# Create your views here.
