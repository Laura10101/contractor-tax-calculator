from django import template
from datetime import datetime

def datestring(value):
    if value is None:
        return ''
    try:
        input_datetime = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%fZ")
    except:
        input_datetime = datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ")
    return input_datetime.strftime("%d-%m-%Y %H:%M:%S")

register = template.Library()
register.filter("datestring", datestring)