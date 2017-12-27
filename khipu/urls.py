try:
    from django.conf.urls.defaults import url
except ImportError:
    from django.conf.urls import url
from .views import verificacion


urlpatterns = [
    url(r'^verificacion/$', verificacion, name='khipu_verificacion'),
]
