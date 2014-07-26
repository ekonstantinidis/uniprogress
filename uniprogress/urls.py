from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

from django.views.generic import TemplateView

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'uniprogress.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', 'membership.views.homepage', name="home"),
    url(r'^about/', TemplateView.as_view(template_name='about.html'), name="about"),
    url(r'^contact/', include('contact.urls')),
    url(r'^membership/', include('membership.urls')),
    url(r'^membership/', include('django.contrib.auth.urls')),
    url(r'^studies/', include('studies.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
