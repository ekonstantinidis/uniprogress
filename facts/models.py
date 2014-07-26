from django.db import models


# Facts Model.
# the 'fact' contains text.
# the 'author' field accepts up to 30 characters
# the 'website' field accepts up to 50 characters
class Fact(models.Model):
    fact = models.TextField()
    author = models.CharField(max_length=30)
    website = models.CharField(max_length=50)

    def __str__(self):
        return self.fact
