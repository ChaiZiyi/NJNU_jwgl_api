from django.conf.urls import url
from django.conf import settings
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^info$', views.info, name='info'),
    url(r'^login$', views.login, name='login'),
    url(r'^scores$', views.scores, name='scores'),
    url(r'^schedule$', views.schedule, name='schedule'),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.STATIC_URL}),
    url(r'', views.others, name='others'),
]
