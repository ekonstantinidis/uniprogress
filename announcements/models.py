from django.db import models


# The announcement model will have 3 attributes
# Title: the title of the announcement
# Text: the content of the announcement
# Date: the date that the announcement will be shown to students
class Announcement(models.Model):
    title = models.CharField(max_length=150)
    text = models.TextField(max_length=500)
    date = models.DateTimeField()
