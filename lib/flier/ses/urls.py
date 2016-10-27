from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'(?P<topic>.+)', views.notify, name='flierses_notify'),
]
