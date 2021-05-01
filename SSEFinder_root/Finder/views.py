from django import forms
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render,redirect
from django.views.generic import TemplateView, View
from Finder.models import Member, Case, Event
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
                return redirect('homepage')
            else:
                return render(request,self.template_name,{'form':form})
        else:
            return render(request,self.template_name,{'form':form})

class AddNewCaseForm(forms.ModelForm):
    class Meta:
        model = Case
        fields = ['caseNumber', 'personName', 'identityDocumentNumber', 'birthDate', 'symptomsOnsetDate', 'infectionConfirmationDate']

    def clean_code(self):
        return self.cleaned_data['caseNumber'].upper()
            
    
class AddNewCase(TemplateView):
    form_class = AddNewCaseForm
    template_name = "addNewCase.html"

    def get(self, request):
        return render(request, self.template_name, {'form': self.form_class})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_case = form.save()
            return redirect("addNewEvent")
        else:
            return render(request, self.template_name, {'form': form})
 
 class AddNewEventForm(forms.ModelForm):
    class Meta:
        model = Event
        exclude = ['venueAddress','venueXCoordinates','venueYCoordinates']

    def clean_code(self):
        return self.cleaned_data['venueName'].upper()

class AddNewEvent(TemplateView):
    form_class = AddNewEventForm
    template_name = "addNewEvent.html"

    def get(self, request):
        return render(request, self.template_name, {'form': self.form_class})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            #check if the event has already exists or not

            try : 
                obj = Event.objects.get(venueName = )
            except : 
                obj = None
            
            if (obj == None) :
                 



            new_event = form.save()
            return redirect("/")
        else:
<<<<<<< HEAD
            return render(request, self.template_name, {'form': form})
            
    
=======
            return render(request, self.template_name, {'form': form})
>>>>>>> f00f77ef6331b38331ffe225a2329f3bb51e3302
