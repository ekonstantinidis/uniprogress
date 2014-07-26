from django import forms


# In this file i'm declaring the fields of the
# contact form so that Django can validate the
# data send through the form.
class ContactForm(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)
