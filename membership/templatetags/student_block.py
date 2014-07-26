from django import template
from studies.models import Student
register = template.Library()


# This template tag is the 'block' informing the student of
# his course and year of studies. It shows up on every page
# with a sidebar(calendar,events, modules etc.)
def student_block(request):
    # Setting the progress to '50'.
    progress = 50

    username = request.user.username
    user_id = request.user.id

    # Checking if the user is enrolled to a course and year
    try:
        studying_course = Student.objects.get(user__id=user_id).course
        studying_year = Student.objects.get(user__id=user_id).year
    except Student.DoesNotExist:
        studying_course = None
        studying_year = None

    # Ιf the user is enrolled, the his progress to registration is 100%
    if studying_year and studying_course:
        progress += 50

    # Return some parameters like the progress, course, year and username to be displayed in the tempate
    return {'progress': progress, 'course': studying_course, 'year': studying_year, 'username': username}

register.inclusion_tag('studies/student_block.html')(student_block)