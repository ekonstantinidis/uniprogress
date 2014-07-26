from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login
from django.template import RequestContext
from django.core import serializers
from forms import RegistrationForm, SelectCourseYear
from studies.models import University, Course
from django.shortcuts import render_to_response


# The view for registering a user
def register_user(request):
    args = {}
    # If the user has submitted the form
    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        # If data are valid(compared to fields in forms.py)
        if form.is_valid():
            # Save the user
            form.save()
            # Login the user
            login_user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
            login(request, login_user)
            # Redirect to the dashboard
            return HttpResponseRedirect(reverse('dashboard'))
    # If the user has NOT submitted the form, return the empty form
    else:
        form = RegistrationForm()

    # Return the form passing arguments. If the user has not submit
    # the form then arguments will be the form
    args['form'] = form
    return render(request, 'home.html', args)


# The view for registering a user
def enroll(request):
    user = request.user
    # If the user has submitted the form
    if request.method == 'POST':
        form = SelectCourseYear(request.POST)
        # If the data are valid
        if form.is_valid():
            # Save the 'student' instance but wait until
            student = form.save(commit=False)
            # ... Until 'student' is related to the logged in usr
            student.user = request.user
            # Finally save
            student.save()
            # Pass a message that enrollment has been successful
            from django.contrib import messages
            messages.success(request, 'You have been successfully enrolled. From now on everything should be organized!')
        return redirect('studies.views.dashboard')
    else:
        form = SelectCourseYear()
    return render(request, 'registration/step3.html',)

# Previous version of registration
def complete(request):
    return render(request, 'registration/complete.html')

# Ιf the user is logged in go to dashboard view(there if not enrolled show enrollment form)
# If not logged in, then show home page(includes registration form
def homepage(request):
    if request.user.is_authenticated():
        return redirect('studies.views.dashboard')
    else:
        return render_to_response("home.html",  RequestContext(request))

# AJAX request. For a particular university, return all courses
def get_university_courses(request, university):
    current_university = University.objects.get(pk=university).pk
    courses = Course.objects.filter(university=current_university)
    if request.is_ajax():
        data = serializers.serialize('json', courses)
        return HttpResponse(data, content_type="application/javascript")


# AJAX request. For a particular course, return all modules
def get_course_years(request, course):
    years = Course.objects.get(pk=course).years
    return HttpResponse(years, mimetype="application/javascript")