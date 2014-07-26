from django.contrib import admin
from announcements.models import Announcement


# In the backend, Announcement will be displayed by
# their title and date. Admins will be able to search
# within titles and there will be a filter for dates
class AnnouncementsAdmin(admin.ModelAdmin):
    list_display = ('title', 'date')
    search_fields = ['title']
    list_filter = ['date']
admin.site.register(Announcement, AnnouncementsAdmin)