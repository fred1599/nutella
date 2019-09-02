from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def form_aliment(aliment):
    html = \
        """
        <a href='{url}'>{name}</a>
        <p>score: {sc}</p>
        """.format(
            url=aliment.url,
            name=aliment.name,
            sc=aliment.score,
            aliment_name=aliment.name
        )

    return mark_safe(html)
