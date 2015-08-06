from django import template
from django.core.urlresolvers import reverse

register = template.Library()

@register.simple_tag
def navactive(request, urls, user_id=0):
    if user_id == 0:
        if request.path in ( reverse(url) for url in urls.split() ):
            return "active"
    else:
        if request.path in ( reverse(url, kwargs={'pk':user_id}) for url in urls.split() ):
            return "active"
    return ""
