from django.conf.urls import patterns, url


urlpatterns = patterns('',
    # Login user. Used when the user submits the login form
    (r'^login$', 'django.contrib.auth.views.login'),
    # Logging out the user
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': 'home'}, name='logout'),

    # The 'Password Reset' page in case users forgotten their password.
    # Also pages for the reset and confirmation.
    url(r'^password/reset/$', 'django.contrib.auth.views.password_reset',
            {'post_reset_redirect' : '/membership/password/reset/done/'}, name='password_reset'),
    (r'^password/reset/done/$', 'django.contrib.auth.views.password_reset_done'),
    (r'^user/password/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
            'django.contrib.auth.views.password_reset_confirm',
            {'post_reset_redirect' : '/password/done/'}),
    (r'^password/done/$', 'django.contrib.auth.views.password_reset_complete'),

    # Registration, Enrolment and Successful Enrollment pages
    url(r'^register/$', 'membership.views.register_user', name="register"),
    url(r'^enroll/$', 'membership.views.enroll', name="enroll"),
    url(r'^step/completed/$', 'membership.views.complete', name="complete"),

    # Ajax, Getting courses for a particular university and modules for a particular course
    # Called from javascript and each one passes the id argument to their view and return the results
    url(r'^university/(?P<university>[-\w]+)/get_university_courses/$', 'membership.views.get_university_courses', name="get_university_courses"),
    url(r'^course/(?P<course>[-\w]+)/get_course_years/$', 'membership.views.get_course_years', name="get_course_years"),
)