from datetime import datetime, timedelta
from django import template
from django.forms.models import model_to_dict


register = template.Library()

@register.simple_tag(name='infector')
def possible_infector(dt_event,dt_onset,dt_confirm):
    Three_days_before = dt_onset-timedelta(days=3)
    gap = dt_confirm-Three_days_before
    for i in range(0, gap.days+1):
        new_date = Three_days_before + timedelta(days=i)
        if new_date == dt_event:
            return True
        else:
            continue
    return False

@register.simple_tag(name='infected')
def possible_infected(dt_event,dt_case):
    for i in range(2, 15): # develop symptoms 2 to 14 days after dt_event
        new_date = dt_event + timedelta(days=i)
        if new_date == dt_case:
            return True
        else:
            continue
    return False

@register.simple_tag(name='SSECheck')
def SSE(event):
    event_dict = model_to_dict(event)
    people = event_dict['people']
    no_of_infected = 0 
    no_of_infectors = 0
    for p in people:
        person_dict = model_to_dict(p)
        print(person_dict)
        if possible_infected(event_dict['eventDate'], person_dict['symptomsOnsetDate']):
            no_of_infected+=1
    if no_of_infected >= 6:
        return True
    else:
        return False
