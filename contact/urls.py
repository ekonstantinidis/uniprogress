from django.conf.urls import patterns, url
from django.views.generic import TemplateView


# Here i'm declaring 2 URL patterns.
# First the '/contact/' url will display the view 'contact.views.contact'
# Then if the data on the form are valid the form will be submit and the
# user will see the '/thanks/' screen which basically is the template
# 'contact/contact-thanks.html'.
urlpatterns = patterns('',
    url(r'^$', 'contact.views.contact', name="contact"),
    url(r'^thanks/$', TemplateView.as_view(template_name='contact/contact-thanks.html'), name="contact-thanks"),
)