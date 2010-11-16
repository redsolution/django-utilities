# -*- coding: utf-8 -*-
from datetime import date, timedelta, datetime
from django import template
from django.utils import dateformat
from django.utils.translation import ugettext_lazy as _

MONTHS = [
    _(' January'), _(' February'), _(' March'), _(' April'), _(' May'),
    _(' June'), _(' July'), _(' August'), _(' September'), _(' October'),
    _(' November'), _(' December')
]

register = template.Library()


class DateFormatLocal(dateformat.DateFormat):

    def F(self):
        "Month, textual, long; e.g. 'January'"
        return MONTHS[self.data.month - 1]


def format(value, format_string):
    "Convenience function"
    df = DateFormatLocal(value)
    return df.format(format_string)

@register.filter(name='date_local')
def date_local(value, arg=None):
    """Formats a date according to the given format."""
    if not value:
        return u''
    if arg is None:
        arg = settings.DATE_FORMAT
    try:
        return format(value, arg)
    except AttributeError:
        return ''
date_local.is_safe = False
