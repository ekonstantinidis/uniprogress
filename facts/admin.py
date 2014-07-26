from django.contrib import admin
from facts.models import Fact

# The backend for managing studying facts(did you know?)
# Shows some attributes.
# Can search for fact and author.
# Can filter authors.


class FactsAdmin(admin.ModelAdmin):
    list_display = ('id', 'fact', 'author', 'website')
    search_fields = ['fact', 'author']
    list_filter = ['author']
admin.site.register(Fact, FactsAdmin)