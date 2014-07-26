import datetime
from django import template
from studies.models import Student, Module, Event
register = template.Library()


# Template tag that shows all the particular upcoming events for a student(enrolled)
def upcoming_events(request):
    # Get logged in user id.
    user_id = request.user.id
    error = ""

    # See if user already enrolled to a course and year
    try:
        studying_course = Student.objects.get(user__id=user_id).course
        studying_year = Student.objects.get(user__id=user_id).year
    except Student.DoesNotExist:
        studying_course = None
        studying_year = None
        error = "Have you selected your University and Course? If not, please complete your profile."

    # Get all the modules for that particular course and year
    try:
        modules = Module.objects.filter(year=studying_year)
    except Module.DoesNotExist:
        modules = None

    # Get up to 3 events/tasks that take place from now on
    now = datetime.datetime.now()
    events = Event.objects.filter(module_id__in=modules, date__gte=now).order_by('date')[:3]
    if (not events) and (not error):
        error = "Oops! It seems that there aren't any upcoming tasks/events."

    return {'course': studying_course, 'year': studying_year, 'events': events, 'error': error}


register.inclusion_tag('studies/upcoming_events_block.html')(upcoming_events)