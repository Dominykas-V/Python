from django import template
register = template.Library()

@register.filter
def samestr(str1, str2):
    if str(str1) == str(str2):
        return True
    else:
         return False