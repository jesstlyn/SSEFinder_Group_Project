from django import forms
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render,redirect
from django.views.generic import TemplateView, View
from Finder.models import Member, Case
from django.contrib import messages

class homePage(TemplateView):
    template_name = 'homePage.html'

class searchCaseNumber(TemplateView):
    template_name = 'searchCaseNumber.html'

class caseNumberDetail(TemplateView):
    model = Case
    template_name = 'caseNumberDetail.html'
    def get_context_data(self, **kwargs):
        query = self.request.GET.get('case_number')
        context = super().get_context_data(**kwargs)

        try :
            caseInfo = Case.objects.get(caseNumber = query)
        except:
            caseInfo = ''

        if (caseInfo == ''):
            context['message'] = "Data Not Found. Please select another location!"
        else:
            caseInfo = Case.objects.get(caseNumber = query)
            context['message'] = "Data Not Found. Please select another location!"
            context['caseNumber'] ="Showing details of case number " + caseInfo.caseNumber
            context['personName'] ="Name: " + caseInfo.personName
            context['identityDocumentNumber'] ="ID Number: " + caseInfo.identityDocumentNumber
            context['birthDate'] ="Birth Date: " + caseInfo.birthDate
            context['symptomsOnsetDate'] ="Symptoms Onset Date: " + caseInfo.symptomsOnsetDate
            context['infectionConfirmationDate'] ="Infection Confirmation Date: " + caseInfo.infectionConfirmationDate

        return context


class LoginForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['username','password']
    
# Create your views here.
class Login(TemplateView):
    form_class = LoginForm
    template_name = "login.html"

    def get(self, request):
        return render(request,self.template_name,{'form':self.form_class})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            member_details = Member.objects.get(username=username)
            if password == member_details.password:
                return redirect('/home')
            else:
                return render(request,self.template_name,{'form':form})
        else:
            return render(request,self.template_name,{'form':form})
    