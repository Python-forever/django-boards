from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter
def field_type(bound_field):
    return bound_field.field.widget.__class__.__name__


@register.filter
def input_class(bound_field):
    css_class = ''
    if bound_field.form.is_bound:
        if bound_field.errors:
            css_class = 'is-invalid'
        elif field_type(bound_field) != 'PasswordInput':
            css_class = 'is-valid'
    return 'form-control {}'.format(css_class)


@register.simple_tag
# @register.filter(name='cut')
# @stringfilter
def cut(post):
    #gender = post.created_by.usergender.get(foruser_id=post.created_by_id).gender
    gender = post.created_by.usergender.get(foruser_id=post.created_by_id).gender
    # if gender == 'Male':
    #     return True
    # else:
    #     return False
    return gender
