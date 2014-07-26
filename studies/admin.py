from django.contrib import admin
from studies.models import University, Course, Module, Event, Student
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

# Here I declare which attributes of each model
# has to be displayed in the backend.
# All attributes are clear enough by their name.


# For Courses admin panel
class CourseAdmin(admin.ModelAdmin):
    # What attributes to display
    list_display = ('name', 'degree', 'years', 'attendance', 'university')
    # Which attributes will be 'searchable'
    search_fields = ['name']
    # Filter those attributes
    list_filter = ['attendance', 'degree']
admin.site.register(Course, CourseAdmin)


class ModuleAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'year')
    search_fields = ['name', 'code']
    list_filter = ['year']
admin.site.register(Module, ModuleAdmin)


class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'date', 'location', 'module')
    search_fields = ['title']
admin.site.register(Event, EventAdmin)


class UniversityAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'website')
    search_fields = ['name']
    list_filter = ['city']
admin.site.register(University, UniversityAdmin)


class StudentAdmin(admin.StackedInline):
    model = Student
    verbose_name_plural = 'students'


# Define a new User Administration System
# And add the 'Student' Admin.
class UserAdmin(UserAdmin):
    inlines = (StudentAdmin,)

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
