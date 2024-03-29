from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings

from rango import views

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'tango_with_django_project.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^rango/', include('rango.urls', namespace='rango')),
    url(r'^admin/', include(admin.site.urls)),
)


if settings.DEBUG:
    urlpatterns += patterns('django.views.static',
        (r'media/(?P<path>.*)','serve',{'document_root': settings.MEDIA_ROOT}),
    )