from django import template


register = template.Library()

@register.filter(name="add_id")
def add_id(value):
    value +=  1
    return value

@register.filter(name="sub_id")
def subtract_id(value):
    value -=  1
    if value < 0:
        return 0
    return value