from datetime import timedelta

from django.core.exceptions import PermissionDenied
from django.utils import timezone

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import DetailView, CreateView
from django.views.generic import ListView
from django.views.generic import TemplateView

from apps.account.models import City
from apps.core.views import CacheMixin
from apps.menu.models.meal import Meal
from apps.order.models import Order, Coupon, CouponUsed
from apps.restaurant.models import Restaurant, Review


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


class CreateOrderView(LoginRequiredMixin, CreateView):
    model = Order
    fields = ['order_time']
    template_name = 'website/order.html'

    def get_success_url(self):
        return reverse('restaurant', kwargs={"pk": self.kwargs['restaurant_pk']})

    def form_valid(self, form):
        object = form.save(commit=False)
        meal = get_object_or_404(Meal, pk=self.kwargs["meal_pk"])
        now_time = timezone.now() + timedelta(minutes=50)
        if object.order_time < now_time:
            form.add_error('order_time', "Order time cannot be sooner than 55 minutes!")
            return self.form_invalid(form)
        object.user = self.request.user
        object.restaurant = meal.menu.restaurant
        object.meal_name = meal.title
        object.meal_price = meal.price
        coupon_used = None
        if self.request.POST.get("coupon_code", ""):
            code = self.request.POST["coupon_code"].upper()
            if Coupon.objects.filter(code=code).exists():
                coupon = Coupon.objects.get(code=code)
                if CouponUsed.objects.filter(user=self.request.user,
                                             coupon=coupon,
                                             restaurant=meal.menu.restaurant).exists():
                    form.add_error(None, "You used this coupon for this restaurant already!")
                    return self.form_invalid(form)
                else:
                    object.meal_price = object.meal_price * ((100.0 - coupon.discount) / 100)

                    coupon_used = CouponUsed(coupon=coupon, restaurant=meal.menu.restaurant, user=self.request.user)

            else:
                form.add_error(None, "Coupon doesn't exist!")
                return self.form_invalid(form)

        meal.order_count = F('order_count') + 1
        meal.save()
        messages.add_message(self.request, messages.SUCCESS, "You've just ordered %s" % meal.title)
        redirect = super(CreateOrderView, self).form_valid(form)
        if coupon_used is not None:
            coupon_used.order = object
            print(coupon_used)
            coupon_used.save()
        return redirect

    def get_context_data(self, **kwargs):
        context = super(CreateOrderView, self).get_context_data(**kwargs)
        context['meal'] = Meal.objects.get(pk=self.kwargs["meal_pk"])
        return context


class OrderListView(LoginRequiredMixin, ListView):
    model = Order

    template_name = "website/orders.html"

    def get_queryset(self):
        return super(OrderListView, self).get_queryset().filter(user=self.request.user)


class CancelOrderView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        order = Order.objects.get(id=self.kwargs["pk"])
        if order.user != request.user:
            raise PermissionDenied
        if order.status == Order.NEW:
            order.status = Order.CANCELLED_BY_CLIENT
            order.save(update_fields=["status"])
        return redirect("orders")


class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    fields = ['comment', 'rate']
    template_name = "website/review.html"

    def dispatch(self, request, *args, **kwargs):
        if Review.objects.filter(author=request.user, restaurant_id=self.kwargs['restaurant_pk']).exists():
            return redirect(self.get_success_url())
        return super(ReviewCreateView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('restaurant', kwargs={"pk": self.kwargs['restaurant_pk']})

    def form_valid(self, form):
        object = form.save(commit=False)
        object.author = self.request.user
        object.restaurant_id = self.kwargs['restaurant_pk']
        return super(ReviewCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ReviewCreateView, self).get_context_data(**kwargs)
        context['restaurant'] = get_object_or_404(Restaurant, pk=self.kwargs['restaurant_pk'])
        return context
