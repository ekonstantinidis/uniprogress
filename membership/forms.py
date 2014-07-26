from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import MinValueValidator, MaxValueValidator
from studies.models import Student, Module


# User Registration form.
# Asks for username, email, and password (with confirmation)
# from the User model
class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    # Validation of the email field.
    # The email address has to be unique.
    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')

        if email and User.objects.filter(email=email).exclude(username=username).count():
            raise forms.ValidationError('This email address is already in use.'
                                        'Please supply a different email address.')
        return email

    # Save the user model if it valid (takes place in the view)
    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user

# The form for selecting university.
# It's a select dropdown so there is no validation
class SelectUniversity(forms.Form):
    university = forms.CharField()


# Enroll to a course and select a year of studies
# There are two AJAX select dropdowns so there is no need
# for validation
class SelectCourseYear(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['course', 'year'] # removing user. we'll handle that in view