from django import template


register = template.Library()

@register.filter
def url_to_str(url):
    return url.replace("/","X")