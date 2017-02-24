from django import forms
from django.core.exceptions import ValidationError
from taggit.models import Tag

from apps.taggit_autocomplete.widgets import TagAutocomplete


class TagField(forms.MultipleChoiceField):
    def __init__(self, choices=(), required=True, widget=None, label=None,
                 initial=None, help_text='', *args, **kwargs):
        choices = Tag.objects.values_list("name", "name")
        super(TagField, self).__init__(choices, False, TagAutocomplete, label, initial, help_text, *args, **kwargs)

    def validate(self, value):
        """
        Validates that the input is a list or tuple.
        """
        if self.required and not value:
            raise ValidationError(self.error_messages['required'], code='required')
