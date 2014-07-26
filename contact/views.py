from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.mail import send_mail
from contact.forms import ContactForm


# This is the view for the contact form.
def contact(request):
    args = {}
    # If the form is submitted
    if request.method == 'POST':
        form = ContactForm(request.POST)
        # If the data submitted are valid
        if form.is_valid():
            # Get the data from the form
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            recipients = ['ekonstantinidis@outlook.com']

            # Submit the email
            send_mail(name, email, message, recipients)

            # Redirect to thank the user for getting in touch
            return HttpResponseRedirect(reverse('contact-thanks'))

    # If the form is not submitted, load the contact form
    else:
        form = ContactForm()

    # If the form is not submitted for any reason,
    # return any possible errors or display the form
    args['form'] = form
    return render(request, 'contact/contact-form.html', args)
