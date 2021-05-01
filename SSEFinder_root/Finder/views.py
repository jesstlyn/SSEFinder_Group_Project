from django.shortcuts import render
from django.views.generic import TemplateView, View
from django.contrib import messages






class AddNewCase(TemplateView):
    form_class = AddNewClassForm
    template_name = "addNewCase.html"

    def get(self, request):
        return render(request, self.template_name, {'form': self.form_class})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_case = form.save()
            return redirect("/")
        else:
            return render(request, self.template_name, {'form': form})


class AddNewCaseForm(forms.ModelForm):
    template_name = "addNewCase.html"

    class Meta:
        model = Case
        fields = ['caseNumber', 'personName', 'identityDocumentNumber', 'birthDate', 'symptomsOnsetDate', 'infectionConfirmationDate']

    def clean_code(self):
        return self.cleaned_data['caseNumber'].upper()