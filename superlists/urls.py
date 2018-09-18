from django.conf.urls import include, url
from django.urls import path
from lists import views as list_views
from lists import urls as list_urls
from accounts import urls as accounts_urls

urlpatterns = [
    url(r'^$', list_views.home_page, name='home'),
    url(r'^lists/', include(list_urls)),
    path('accounts/', include(accounts_urls)),
]

