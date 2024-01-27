from django.template import Library

register = Library()


@register.filter()
def add_url_query_(a, b):
    result = f'{a}'
    if b.get('search'):
        result += f"&search={b['search']}"
    return result
