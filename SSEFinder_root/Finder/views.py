from django import forms
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render,redirect
from django.views.generic import TemplateView, View
from Finder.models import Member, Case, Event
from django.contrib import messages
import json
import requests
import sys

#get data from API
def get_data(venueName):
    xcoord = None
    ycoord = None
    address = None
    url = "https://geodata.gov.hk/gs/api/v1.0.0/locationSearch"
    response = requests.get(url=url,params={"q": venueName})
    response_json = response.json()
    for i in response_json:
        if i['nameEN'] == venueName:
            xcoord = i['x']
            ycoord = i['y']
            address = i['nameEN']
    print(response_json)
    mylist = [xcoord, ycoord, address]
    return mylist

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
                return redirect('/homePage')
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
            form.save()
            return redirect("/addNewEvent")
        else:
            return render(request, self.template_name, {'form': form})
 
class AddNewEventForm(forms.ModelForm):
    class Meta:
        model = Event
        exclude = ['venueAddress', 'venueXCoordinates', 'venueYCoordinates']
    
    # def save(self, commit=True, xcoord = '', ycoord = ''):
    #     obj = super(AddNewEventForm, self).save(commit=False)
    #     obj.venueXCoordinates = xcoord
    #     obj.venueYCoordinates = ycoord
    #     if commit:
    #         obj.save()
    #     return obj

    def clean_code(self):
        return self.cleaned_data['venueName'].upper()

class AddNewEvent(TemplateView):
    form_class = AddNewEventForm
    template_name = "addNewEvent.html"

    def get(self, request):
        return render(request, self.template_name, {'form': self.form_class})

    def post(self, request):
        form = self.form_class(request.POST)
        #self.fields['venueXCoordinates'].widget.attrs['readonly'] = True
        #self.fields['venueYCoordinates'].widget.attrs['readonly'] = True

        if form.is_valid():
            inputVenueName = request.POST['venueName']
            print(inputVenueName)
            venueDetails = get_data(inputVenueName)
            print(venueDetails)

            #check if the event has already exists or not
            try : 
                obj = Event.objects.get(venueName = inputVenueName)
                print(obj)
            except : 
                obj = None

            if (obj == None) :#not exist
                newEvent = form.save(commit=False)
                eventData = get_data(inputVenueName)
                newEvent.venueAddress = venueDetails[2]
                newEvent.venueXCoordinates = venueDetails[0]
                newEvent.venueYCoordinates = venueDetails[1]
                newEvent.numberOfPeople = 1
                newEvent.save()
            else:
                numOfPeople = obj.numberOfPeople
                print("num of ppl in db : ", numOfPeople)
                obj.numberOfPeople = numOfPeople + 1
                obj.save()
            #form(venueXCoordinates='xcoord', venueYCoordinates='ycoord')
            # newEvent = form.save(commit=False)
            # newEvent.venueXCoordinates = xcoord
            # newEvent.venueYCoordinates = ycoord
            # newEvent.save()
            return redirect("/homePage")
        else:
            return render(request, self.template_name, {'form': form})
            
    
class SearchEvent(TemplateView):
    template_name = "searchEvent.html"
    
class EventDetail(TemplateView):
    model = Event
    template_name = 'eventPage.html'
    def get_context_data(self, **kwargs):
        startdate = self.request.GET.get('startdate')
        enddate = self.request.GET.get('enddate')
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



