from django.contrib.auth import login, logout
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.contrib import messages

from django.views.generic import CreateView
from django.views.generic import FormView
from django.views.generic import TemplateView

from apps.account.forms import RegisterForm, LoginForm
from apps.account.models import User, City
from apps.website.views import ListItems


class RegisterView(CreateView):
    model = User
    form_class = RegisterForm
    success_url = "/"
    template_name = "website/register.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(self.success_url)
        return super(RegisterView, self).get(request, *args, **kwargs)

    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR, "There are errors in your form")
        return super(RegisterView, self).form_invalid(form)

    def form_valid(self, form):
        user = form.save(False)
        user.set_password(form.cleaned_data["password1"])
        user.first_name = form.cleaned_data["first_name"]
        user.last_name = form.cleaned_data["last_name"]
        user.city = City.objects.filter(name=form.cleaned_data["city"]).first()
        user.is_staff = True
        user.save()
        g = Group.objects.get(name='Restaurant owner')
        g.user_set.add(user)
        messages.add_message(self.request, messages.SUCCESS, "Now you can log in")
        return HttpResponseRedirect(self.success_url)


class LoginView(FormView):
    form_class = LoginForm
    success_url = "/"
    template_name = "website/login.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(self.success_url)
        return super(LoginView, self).get(request, *args, **kwargs)

    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR, "There are errors in your form")
        return super(LoginView, self).form_invalid(form)

    def form_valid(self, form):
        login(self.request, form.user)
        messages.add_message(self.request, messages.SUCCESS, "Logged in")
        redirect_url = self.get_success_url()
        if "next" in self.request.POST and self.request.POST["next"]:
            redirect_url = self.request.POST["next"]
        return redirect(redirect_url)


class LogoutView(TemplateView):
    success_url = "/"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.add_message(self.request, messages.SUCCESS, "Logged out")
            logout(request)
        return redirect(self.success_url)


class ListCities(ListItems):
    model = City

    def get_queryset(self, key):
        return City.objects.filter(name__icontains=key)

    def get_items(self, request):
        items = None
        if "q" in request.GET:
            items = self.get_queryset(request.GET["q"])
        else:
            items = self.model.objects.all()
        if bool(self.request.GET.get("only_restaurants", "False")):
            items = items.filter(restaurant__isnull=False).distinct()

        return items
