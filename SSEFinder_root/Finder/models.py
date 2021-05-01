
from django.db import models

class Member(models.Model):
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    staffNumber = models.CharField(max_length=200)
    firstName = models.CharField(max_length=200)
    lastName = models.CharField(max_length=200)
    email = models.CharField(max_length=200)

class Case(models.Model):
    caseNumber = models.IntegerField(unique=True)
    personName = models.CharField(max_length=200)
    identityDocumentNumber = models.CharField(max_length = 7)
    birthDate = models.DateField()
    symptomsOnsetDate = models.DateField()
    infectionConfirmationDate = models.DateField()

class Event(models.Model):
    venueName = models.CharField(max_length=200)
    venueLocation = models.CharField(max_length=200)
    venueAddress = models.CharField(max_length=200)
    venueXCoordinates = models.DecimalField(max_digits=10, decimal_places=10)
    venueYCoordinates = models.DecimalField(max_digits=10, decimal_places=10)
    eventDate = models.DateField()
    eventDescriptipn = models.CharField(max_length=200)
    numberOfPeople = models.IntegerField()
    people = models.ManyToManyField(Case, through='CaseEvent')

class CaseEvent(models.Model):
    caseEventNumber =  models.ForeignKey(Case, on_delete=models.CASCADE)
    caseEventVenueId = models.ForeignKey(Event, on_delete=models.CASCADE)
    







