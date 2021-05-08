from datetime import datetime, timedelta
from django import template

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
    for i in range(2, 15): #develop symptoms 2 to 14 days after dt_event
        new_date = dt_event + timedelta(days=i)
        if new_date == dt_case:
            return True
        else:
            continue
    return False