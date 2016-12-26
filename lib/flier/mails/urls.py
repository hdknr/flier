from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^click/(?P<mail>\d+)/(?P<recipient>\d+)/(?P<message_id>.+)',
        views.click, name='fliermails_click'),
]
