from django.http import Http404
from django.http import JsonResponse
from django.views import View
from django.views.generic import TemplateView
from taggit.models import Tag

from apps.website.views import ListItems


class ListTags(ListItems):
    model = Tag

    def get_queryset(self, key):
        return Tag.objects.filter(name__icontains=key).values_list('name', flat=True)
