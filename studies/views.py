import datetime
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.contrib.auth.decorators import login_required
from studies.models import University, Module, Event, Student


# If the user is not logged in go to home page
@login_required(login_url='/')
def dashboard(request):
        # Get the logged in user id and todays date
        user_id = request.user.id
        now = datetime.datetime.today()

        # Check if the user is enrolled
        enrolled = Student.objects.filter(user__id=user_id).count()
        # If the user is enrolled
        if enrolled > 0:
            progress = 50
            studying_course = Student.objects.get(user__id=user_id).course
            studying_year = Student.objects.get(user__id=user_id).year
            # Get all the modules for that course
            try:
                modules = Module.objects.filter(course=studying_course,year=studying_year)
            except Module.DoesNotExist:
                modules = None

            # Get events for today
            events_today = Event.objects.filter(module_id=modules, date__year=now.year, date__month=now.month, date__day=now.day)
            # Get events after today
            events_upcoming = Event.objects.filter(module_id=modules, date__gte=now).exclude(date__year=now.year, date__month=now.month, date__day=now.day).order_by('date')[:3]
            # DEBUGGING using pdb. import pdb; pdb.set_trace()

            return render_to_response("dashboard.html", {'enrolled': enrolled, 'today': events_today, 'upcoming': events_upcoming, 'progress': progress, 'course': studying_course, 'year': studying_year, 'now': now,},  RequestContext(request))
        else:
            universities = University.objects.order_by('name').distinct()
            return render_to_response("dashboard.html", {'enrolled': enrolled, 'universities': universities, 'now': now,},  RequestContext(request))


# The calendar view. Returns all the events of the year and the template will add them to the calendar.
def calendar(request):
    if request.user.is_authenticated():
        user_id = request.user.id

        try:
            studying_course = Student.objects.get(user__id=user_id).course
            studying_year = Student.objects.get(user__id=user_id).year
        except Student.DoesNotExist:
            return HttpResponseRedirect(reverse('step2'))

        modules = Module.objects.filter(course=studying_course,year=studying_year)
        events = Event.objects.filter(module_id__in=modules).order_by('date')

        return render_to_response("studies/calendar.html", {'course': studying_course, 'year': studying_year, 'events': events},  RequestContext(request))

    else:
        return HttpResponseRedirect(reverse('home'))


# Get details for a particular event
def event_details(request, event_id):
    if request.user.is_authenticated():
        event = Event.objects.get(pk=event_id)
        module_obj = Event.objects.get(pk=event_id).module_id
        module_name = Module.objects.get(pk=module_obj)
        return render_to_response("studies/event.html", {'event': event, 'module': module_name},  RequestContext(request))
    else:
        return HttpResponseRedirect(reverse('home'))


# Get all upcoming events for logged in user
def upcoming_events(request):
    if request.user.is_authenticated():
        user_id = request.user.id

        try:
            studying_course = Student.objects.get(user__id=user_id).course
            studying_year = Student.objects.get(user__id=user_id).year
        except Student.DoesNotExist:
            return HttpResponseRedirect(reverse('step2'))

        modules = Module.objects.filter(course=studying_course,year=studying_year)

        # Get events from now on
        now = datetime.datetime.now()
        events = Event.objects.filter(module_id=modules,date__gte=now).order_by('date')

        # Create a pagination. Every page has up to 5 events.
        paginator = Paginator(events, 5)
        try:
            page = int(request.GET.get("page", '1'))
        except ValueError:
            page = 1

        try:
            posts = paginator.page(page)
        except (InvalidPage, EmptyPage):
            posts = paginator.page(paginator.num_pages)

        return render_to_response("studies/upcoming_events.html", {'course': studying_course, 'year': studying_year, 'events': events, 'posts': posts},  RequestContext(request))
    else:
        return HttpResponseRedirect(reverse('home'))


# Gets all the modules for a particular year of a course(student enrolled)
def modules(request):
    if request.user.is_authenticated():
        # Get user's id
        user_id = request.user.id

        # See what course is the user enrolled to
        try:
            studying_course = Student.objects.get(user__id=user_id).course
            studying_year = Student.objects.get(user__id=user_id).year
        except Student.DoesNotExist:
            return HttpResponseRedirect(reverse('step2'))

        # Get all the modules list except those that include 'school'.
        # 'School' modules acts for events like ceremonies and vacation
        # so it should be displayed in the module list
        try:
            modules_list = Module.objects.filter(course=studying_course,year=studying_year).exclude(name="school")
        except Module.DoesNotExist:
            modules_list = None
        # DEBUGGING... import pdb; pdb.set_trace()
        return render_to_response("studies/modules.html", {'course': studying_course, 'year': studying_year, 'modules': modules_list,},  RequestContext(request))

    else:
        return HttpResponseRedirect(reverse('home'))


# Get all the upcoming events for a particular module id
def module_details_upcoming(request, module_id):
    if request.user.is_authenticated():
        user_id = request.user.id
        # Dated will be used in the template implementation to see if it's upcoming or previous
        dated = True

        # See what course is the user enrolled to
        try:
            studying_course = Student.objects.get(user__id=user_id).course
            studying_year = Student.objects.get(user__id=user_id).year
        except Student.DoesNotExist:
            return HttpResponseRedirect(reverse('step2'))

        try:
            module = Module.objects.get(id=module_id)
        except Module.DoesNotExist:
            module = None

        # Get events from now on
        now = datetime.datetime.now()
        events = Event.objects.filter(module=module_id,date__gte=now).order_by('date')

        # Create a pagination. Every page has up to 5 events.
        paginator = Paginator(events, 5)
        try:
            page = int(request.GET.get("page", '1'))
        except ValueError:
            page = 1

        try:
            posts = paginator.page(page)
        except (InvalidPage, EmptyPage):
            posts = paginator.page(paginator.num_pages)

        return render_to_response("studies/module.html", {'module': module, 'events': events, 'posts': posts, 'dated': 'dated'},  RequestContext(request))
    else:
        return HttpResponseRedirect(reverse('home'))


# Get all the previous events for a particular module id
def module_details_previous(request, module_id):
    if request.user.is_authenticated():
        user_id = request.user.id
        # Dated will be used in the template implementation to see if it's previous or upcoming
        dated = False

        # See what course is the user enrolled to
        try:
            studying_course = Student.objects.get(user__id=user_id).course
            studying_year = Student.objects.get(user__id=user_id).year
        except Student.DoesNotExist:
            return HttpResponseRedirect(reverse('step2'))

        module = Module.objects.get(id=module_id)

        # Get events from the past
        now = datetime.datetime.now()
        events = Event.objects.filter(module=module_id,date__lte=now).order_by('date')

        # Create a pagination. Every page has up to 5 events.
        paginator = Paginator(events, 5)
        try:
            page = int(request.GET.get("page", '1'))
        except ValueError:
            page = 1

        try:
            posts = paginator.page(page)
        except (InvalidPage, EmptyPage):
            posts = paginator.page(paginator.num_pages)

        return render_to_response("studies/module.html", {'module': module, 'events': events, 'posts': posts, 'dated': dated,},  RequestContext(request))
    else:
        return HttpResponseRedirect(reverse('home'))