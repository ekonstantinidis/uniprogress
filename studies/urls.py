from django.conf.urls import patterns, url


urlpatterns = patterns('',
    url(r'^dashboard/$', 'studies.views.dashboard', name="dashboard"),
    url(r'^calendar/$', 'studies.views.calendar', name="calendar"),
    url(r'^events/$', 'studies.views.upcoming_events', name="events"),
    url(r'^event/(?P<event_id>\d+)/$', 'studies.views.event_details', name="event_details"),
    url(r'^modules/$', 'studies.views.modules', name="modules"),
    url(r'^module/(?P<module_id>\d+)/upcoming/$', 'studies.views.module_details_upcoming', name="module_details_upcoming"),
    url(r'^module/(?P<module_id>\d+)/previous/$', 'studies.views.module_details_previous', name="module_details_previous"),
)
