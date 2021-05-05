from datetime import datetime, timedelta
from django import template

register = template.Library()

@register.simple_tag(name='infector')
def possible_infector(dt_event,dt_case):
    Three_days_before = dt_case-timedelta(days=3)
    for i in range(0, 4):
        new_date = Three_days_before + timedelta(days=i)
        if new_date == dt_event:
            return True
        else:
            continue
    return False

@register.simple_tag(name='infected')
def possible_infected(dt_event,dt_case):
    Fourteen_days_after = dt_case-timedelta(days=14)
    for i in range(2, 15):
        new_date = Fourteen_days_after + timedelta(days=i)
        if new_date == dt_event:
            return True
        else:
            continue
    return False