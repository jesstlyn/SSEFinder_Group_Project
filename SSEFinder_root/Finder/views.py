from django.shortcuts import render
from django import forms
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render,redirect
from django.views.generic import TemplateView
from Finder.models import Member

class LoginForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['username','password']
    
# Create your views here.
class Login(TemplateView):
    form_class = LoginForm
    template_name = "login.html"

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            member_details = Member.objects.get(username=username)
            if password == Member.password:
                return redirect('/home')
            else:
                return render(request,self.template_name,{'form':form})
        else:
            return render(request,self.template_name,{'form':form})
    