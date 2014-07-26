import datetime
from django import template
from announcements.models import Announcement
register = template.Library()


# The template tag 'announcements_today' filters all
# the announcements and returns a list with todays
# announcements.
# Then this template tag can be shown site-wide.
def announcements_today(request):
    now = datetime.datetime.now()
    try:
        announcements = Announcement.objects.all().filter(date__year=now.year, date__month=now.month, date__day=now.day)
    except Announcement.DoesNotExist:
        announcements = None
    return {'announcements': announcements, }

register.inclusion_tag('announcements/announcements_block.html')(announcements_today)