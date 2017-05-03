from django import template

from apps.restaurant.models import Review

register = template.Library()


@register.filter(takes_context=True)
def has_reviewed(restaurant, user):
    return Review.objects.filter(author=user, restaurant_id=restaurant.id).exists()


@register.filter(takes_context=True)
def is_author(review, user):
    return review.author == user


@register.filter()
def to_rate(max):
    result = []
    if max is None or max == 0:
        return result
    for i in range(0, int(max)):
        result.append({"checked": True})

    for i in range(0, 5 - int(max)):
        result.append({"checked": False})

    return result
