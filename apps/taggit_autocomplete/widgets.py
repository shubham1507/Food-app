from django import forms
from django.db.models import QuerySet
from django.utils.safestring import mark_safe


class TagAutocomplete(forms.SelectMultiple):
    input_type = 'text'

    def render(self, name, value, attrs=None):
        if isinstance(value, QuerySet):
            value = [o.tag for o in list(value)]
        html = super(TagAutocomplete, self).render(name, value, attrs)
        return mark_safe(html)

