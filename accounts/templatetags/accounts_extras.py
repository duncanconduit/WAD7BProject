from django import template
register = template.Library()

@register.simple_tag
def get_avatar_colour(user):
    return user.avatar_gradient