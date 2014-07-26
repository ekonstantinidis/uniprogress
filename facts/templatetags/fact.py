from django import template
from facts.models import Fact
register = template.Library()


# Retrieving a random fact from
# Rendering to 'facts/facts.html'
def random_fact():

    fact = Fact.objects.order_by('?').first()
    return {'fact': fact}

register.inclusion_tag('facts/fact.html')(random_fact)
