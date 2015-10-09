from django.conf.urls import url
import views


urlpatterns = [
    url(r'(?P<topic>.+)', views.notify, name='flierses_notify'),
]
