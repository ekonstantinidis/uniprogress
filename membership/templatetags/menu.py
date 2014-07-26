from django import template
from studies.models import Student, Module, Event
register = template.Library()


# This template tag checks if the user has already
# enrolled to a course so that it loads the proper menu.
# The idea is to hide the 'dashboard' etc from students
# that haven't enroll yet and only allow them to enroll
# in order to continue.
def menu(request):

    user = request.user
    user_id = request.user.id
    enrolled = False

    try:
        studying_course = Student.objects.get(user__id=user_id).course
        studying_year = Student.objects.get(user__id=user_id).year
    except Student.DoesNotExist:
        studying_course = None
        studying_year = None

    if studying_year and studying_course:
        enrolled = True

    return {'enrolled': enrolled, 'user': user,}

register.inclusion_tag('registration/menu.html')(menu)