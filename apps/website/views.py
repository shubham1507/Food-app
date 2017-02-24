from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import TemplateView

from apps.account.models import City
from apps.core.views import CacheMixin
from apps.menu.models.meal import Meal
from apps.order.models import Order
from apps.restaurant.models import Restaurant


class ListItems(CacheMixin, TemplateView):
    items_per_page = 10
    model = None

    def get_queryset(self, key):
        raise NotImplemented()

    def get(self, request, *args, **kwargs):
        page = int(request.GET.get("page", 1))
        items_per_page = self.items_per_page
        if "items_per_page" in request.GET and request.GET["items_per_page"].isdigit():
            items_per_page = int(request.GET["items_per_page"])
        if page < 1:
            page = 1
        items = self.get_items(request)
        start = (page - 1) * items_per_page
        end = page * items_per_page
        return JsonResponse(
            {"items": list(items.order_by("name")[start:end].values_list("name", flat=True)),
             "total_count": items.count(),
             "page": page,
             "next_page": (int(items.count() / items_per_page) + 1) > page,
             "items_per_page": items_per_page
             })

    def get_items(self, request):
        if "q" in request.GET:
            return self.get_queryset(request.GET["q"])
        else:
            return self.model.objects.all()


class IndexView(LoginRequiredMixin, ListView):
    template_name = "website/index.html"
    model = Restaurant

    def get_login_url(self):
        return reverse("login")

    def get_queryset(self):
        queryset = super(IndexView, self).get_queryset()
        city = self.request.user.city
        if "city" in self.request.GET and self.request.GET["city"]:
            city = get_object_or_404(City, name=self.request.GET["city"])
        queryset = queryset.filter(city=city)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        return context


class RestaurantView(LoginRequiredMixin, DetailView):
    model = Restaurant
    template_name = "website/restaurant.html"


class CreateOrderView(LoginRequiredMixin, View):
    model = Order

    def get(self, request, *args, **kwargs):
        meal = Meal.objects.get(pk=kwargs["pk"])
        Order(user=request.user, restaurant=meal.menu.restaurant, meal_name=meal.title, meal_price=meal.price).save()
        messages.add_message(self.request, messages.SUCCESS, "You've just ordered %s" % meal.title)
        return redirect(meal.menu.restaurant)


class OrderListView(LoginRequiredMixin, ListView):
    model = Order

    template_name = "website/orders.html"

    def get_queryset(self):
        return super(OrderListView, self).get_queryset().filter(user=self.request.user)
