from django import template

from rango.views import get_category_list
register = template.Library()

@register.inclusion_tag('rango/category_list.html')
def category(takes_context=True):
    return {"categories": get_category_list()}


