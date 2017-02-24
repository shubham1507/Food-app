from django.conf.urls import url, include
from django.contrib import admin

from apps.account.views import RegisterView, LoginView, LogoutView, ListCities
from apps.taggit_autocomplete.views import ListTags
from apps.website.views import IndexView, RestaurantView, CreateOrderView, OrderListView

urlpatterns = [
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^nested_admin/', include('nested_admin.urls')),
    url(r'', include('taggit_live.urls')),
    url(r'^list_tags/$', ListTags.as_view(), name='list_tags'),
    url(r'^list_cities/$', ListCities.as_view(), name='list_cities'),
    url(r'^orders/$', OrderListView.as_view(), name='orders'),
    url(r'^restaurant/(?P<pk>\d+)/$', RestaurantView.as_view(), name='restaurant'),
    url(r'^order/(?P<pk>\d+)/$', CreateOrderView.as_view(), name='order'),
    url(r'^$', IndexView.as_view(), name="index"),
    url(r'^register/$', RegisterView.as_view(), name="register"),
    url(r'^login/$', LoginView.as_view(), name="login"),
    url(r'^logout/$', LogoutView.as_view(), name="logout"),
]
