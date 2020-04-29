from django import template
from main_object.models import Category, MainObject


register = template.Library()


@register.simple_tag()
def get_categories():
    return Category.objects.all()


@register.inclusion_tag('include/widget_last_add.html')
def get_last_add(count=5):
    objects = MainObject.objects.order_by('id')[:count]
    return {
        'last_add': objects
    }