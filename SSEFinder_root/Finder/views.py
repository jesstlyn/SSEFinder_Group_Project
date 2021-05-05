from django import forms
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render,redirect
from django.views.generic import TemplateView, View
from Finder.models import Member, Case, Event, CaseEvent
from django.contrib import messages
from datetime import datetime,timedelta
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
            context['message'] = "Data for case number '" + query +  "'  is not found. Please input another valid case number!"
        else:
            # caseInfo = Case.objects.get(caseNumber = query)
            # context['message'] = ""
            context['caseNumber'] =  str(caseInfo.caseNumber)
            context['personName'] = caseInfo.personName
            context['identityDocumentNumber'] = caseInfo.identityDocumentNumber
            context['birthDate'] = str(caseInfo.birthDate)
            context['symptomsOnsetDate'] = str(caseInfo.symptomsOnsetDate)
            context['infectionConfirmationDate'] = str(caseInfo.infectionConfirmationDate)

        return context

class CreateAccountForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = '__all__'

class CreateAccount(TemplateView):
    form_class = CreateAccountForm
    template_name = "createAccount.html"

    def get(self, request):
        return render(request, self.template_name, {'form': self.form_class})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/homePage")
        else:
            return render(request, self.template_name, {'form': form})

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
                #give message username/password is wrong 
                msg = "Username or password is not valid. Please input a valid username or password!"
                return render(request,self.template_name,{'form':form, 'message' : msg})
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
            #request.session['web_input'] = request.POST['web_input']
            request.session['caseNumber'] = request.POST['caseNumber']
            form.save()
            return redirect("/addNewEvent")
        else:
            return render(request, self.template_name, {'form': form})
 
class AddNewEventForm(forms.ModelForm):
    class Meta:
        model = Event
        exclude = ['venueAddress','venueXCoordinates','venueYCoordinates', 'people']

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
        caseNumber = request.session.get('caseNumber')
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
                case_object = Case.objects.get(caseNumber= caseNumber)
                event = Event.objects.get(venueName=inputVenueName) #first get the object
                event.people.add(case_object)
            else:
                numOfPeople = obj.numberOfPeople
                print("num of ppl in db : ", numOfPeople)
                obj.numberOfPeople = numOfPeople + 1
                #save another persons pkey and event in the middle table here
                obj.save()
                case_object = Case.objects.get(caseNumber= caseNumber)
                event = Event.objects.get(venueName=inputVenueName) #first get the object
                event.people.add(case_object)
            #form(venueXCoordinates='xcoord', venueYCoordinates='ycoord')
            # newEvent = form.save(commit=False)
            # newEvent.venueXCoordinates = xcoord
            # newEvent.venueYCoordinates = ycoord
            # newEvent.save()
            return redirect("/addNewEvent")
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
        start = datetime.fromisoformat(startdate).date()
        end = datetime.fromisoformat(enddate).date()
        gap = datetime.fromisoformat(enddate) - datetime.fromisoformat(startdate)
        date_list = []
        for day in range(0,gap.days):
            new_date = datetime.fromisoformat(startdate) + timedelta(days=day)
            date_list.append(new_date)
        
        context = super().get_context_data(**kwargs)

        events = {}
        for day in date_list:
            date_of_event = day.date()
            try:
                events_in_that_day = Event.objects.filter(eventDate = date_of_event)
                date_string = date_of_event.strftime("%Y-%m-%d")
                events[date_string] = events_in_that_day
            except:
                continue

        
        context['event_list'] = events 
        context['startdate'] = startdate
        context['enddate'] = enddate

        return context



