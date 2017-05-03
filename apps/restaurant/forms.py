from django import forms

from apps.menu.models.meal import Meal
from apps.taggit_autocomplete.form_fields import TagField
from apps.taggit_autocomplete.widgets import TagAutocomplete


class MealForm(forms.ModelForm):
    tags = TagField()

    def __init__(self, *args, **kwargs):
        super(MealForm, self).__init__(*args, **kwargs)
        tags = self.fields['tags']
        tags.widget.attrs['class'] = 'tags'

    class Meta:
        model = Meal
        fields = ["title", "price", "tags", "image"]
        widgets = {
            'tags': TagAutocomplete(),
        }
