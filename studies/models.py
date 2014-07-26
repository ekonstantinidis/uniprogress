from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User


# That is where I declare all the tables and attributes.
# Django ORM will get the models and create and manipulate the data
class University(models.Model):
    # Declaring the attributes of the model 'University'
    name = models.CharField(max_length=75)
    city = models.CharField(max_length=50)
    website = models.CharField(max_length=35,
                               blank=True)

    # The 'plural' for university
    class Meta:
        verbose_name_plural = "Universities"

    def __unicode__(self):
        return self.name


class Course(models.Model):
    # Setting attendance to either 'Full Time' and 'Part Time'
    TYPE_OF_ATTENDANCE_CHOICES = (
        ('FT', 'Full Time'),
        ('PT', 'Part Time'),
    )

    name = models.CharField(max_length=100)
    years = models.IntegerField(validators=[MinValueValidator(1),
                                            MaxValueValidator(7)])
    degree = models.CharField(max_length=15)
    attendance = models.CharField(max_length=2,
                                  choices=TYPE_OF_ATTENDANCE_CHOICES,
                                  default='FT')
    university = models.ForeignKey(University)
    modules = models.ManyToManyField('Module', blank=True)

    # When returning a course object, show its name and degree (ie. Computer Science, BSc(Hons))
    def __unicode__(self):
        return "%s, %s" % (self.name, self.degree)

    # When aksing for 'course_info' of a course object, show its name and degree (ie. Computer Science, BSc(Hons))
    def course_info(self):
        return "%s, %s" % (self.name, self.degree)


class Module(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=65)
    year = models.IntegerField(validators=[MinValueValidator(0),
                                           MaxValueValidator(7)])

    # When returning a Module object, show its code and name (ie. CI347 - Web & Network Management)
    def __unicode__(self):
        return "%s - %s" % (self.code, self.name)

    # Whens asking for the degree of a module, then find it's course and then show it's degree
    def degree(self):
        return self.course.degree


class Event(models.Model):
    # Type of event. Can be 'Lecture', 'Lab' etc.
    TYPE_OF_EVENT_CHOICES = (
        ('LE', 'Lecture'),
        ('LA', 'Lab'),
        ('CW', 'Coursework'),
        ('EX', 'Exam'),
        ('PR', 'Presentation'),
        ('OT', 'Other'),
    )

    # Attributes of the Event model
    title = models.CharField(max_length=100)
    type = models.CharField(max_length=2,
                            choices=TYPE_OF_EVENT_CHOICES,
                            default='CW')
    date = models.DateTimeField()
    location = models.CharField(max_length=60)
    description = models.TextField()
    module = models.ForeignKey(Module)


# The Student Model.
class Student(models.Model):
    # Each student is linked to exactly one User of the Django auth system
    user = models.OneToOneField(User)
    # Each student is linked to a course. Many students belong to many courses
    course = models.ForeignKey(Course)
    # Year of studies. Can be an integer from 1 to 7.
    # During the selection of the year, the form is AJAX. So worst case, year 7, part time bachelor degree
    year = models.IntegerField(validators=[MinValueValidator(1),
                                           MaxValueValidator(7)])