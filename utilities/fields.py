# -*- coding: utf-8 -*-

from django import forms
from django.db import models
from django.contrib.admin.widgets import AdminFileWidget
from django.utils import dates
from utilities.widgets import ImagePreviewWidget
import datetime

class ImagePreviewFormField(forms.ImageField):
    widget = ImagePreviewWidget

class ImagePreviewField(models.ImageField):
    def __init__(self, thumb_field=None, thumb_size=(80, 80), *args, **kwargs):
        """
        ``thumb_field`` name of field with thumb image. If None will use image itself.
        ``thumb_size`` maximum (width, height) to be displayed. If None original size will be used.
        """
        self.thumb_field = thumb_field
        self.thumb_size = thumb_size
        super(ImagePreviewField, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        defaults = {'widget': ImagePreviewWidget}
        defaults.update(kwargs)

        # As an ugly hack, we override the admin widget
        if defaults['widget'] == AdminFileWidget:
            defaults['widget'] = ImagePreviewWidget

        if defaults['widget'] == ImagePreviewWidget:
            defaults['widget'] = ImagePreviewWidget(thumb_field=self.thumb_field, thumb_size=self.thumb_size)

        return super(ImagePreviewField, self).formfield(**defaults)

try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([
        (
            [ImagePreviewField],
            [],
            {
                "thumb_field": ["thumb_field", {"default": None}],
                "thumb_size": ["thumb_size", {"default": (80, 80)}],
            },
        ),
    ], [
        "^utilities\.fields\.ImagePreviewField",
    ])
except ImportError:
    pass

#    SplitDateField
EMPTY = [('', u'---')]
DAYS = [(day, '%02d' % day) for day in xrange(1, 32)]
MONTHS = [(month, dates.MONTHS[month]) for month in xrange(1, 13)]
DEFAULT_FROM_YEAR = 1930

def widget_factory(years):
    class SplitDateWidget(forms.MultiWidget):
        def __init__(self, attrs=None):
            widgets = (
                forms.Select(attrs=None, choices=EMPTY + DAYS),
                forms.Select(attrs=None, choices=EMPTY + MONTHS),
                forms.Select(attrs=None, choices=EMPTY + years),
            )
            super(SplitDateWidget, self).__init__(widgets, attrs)

        def decompress(self, value):
            if value:
                return [value.day, value.month, value.year]
            return [None, None, None]
    return  SplitDateWidget

class SplitDateFormField(forms.MultiValueField):

    def __init__(self, from_date=datetime.date(DEFAULT_FROM_YEAR, 01, 01),
        till_date=datetime.date.today, reverse=False, *args, **kwargs):
        if callable(from_date):
            from_date = from_date()
        if callable(till_date):
            till_date = till_date()
        self.from_date = from_date
        self.till_date = till_date
        from_year = from_date.year
        till_year = till_date.year
        years = [(year, '%04d' % year) for year in xrange(till_year,
            from_year - 1, -1)]
        if reverse:
            years.reverse()
        errors = self.default_error_messages.copy()
        if 'error_messages' in kwargs:
            errors.update(kwargs['error_messages'])
        kwargs['widget'] = widget_factory(years)
        fields = (
            forms.ChoiceField(choices=DAYS),
            forms.ChoiceField(choices=MONTHS),
            forms.ChoiceField(choices=years),
        )
        super(SplitDateFormField, self).__init__(fields, *args, **kwargs)

    def compress(self, value_list):
        if value_list:
            for value in value_list:
                if value in forms.fields.EMPTY_VALUES:
                    raise forms.ValidationError(forms.SplitDateTimeField.default_error_messages['invalid_date'])
            kwargs = {
                'day': int(value_list[0]),
                'month': int(value_list[1]),
                'year': int(value_list[2]),
            }
            try:
                date = datetime.date(**kwargs)
                if date > self.till_date or date < self.from_date:
                    raise forms.ValidationError(forms.SplitDateTimeField.default_error_messages['invalid_date'])
                else:
                    return date
            except ValueError:
                raise forms.ValidationError(forms.SplitDateTimeField.default_error_messages['invalid_date'])
        return None

class SplitDateField(models.DateField):
    def __init__(self, from_date=datetime.date(DEFAULT_FROM_YEAR, 01, 01),
        till_date=datetime.date.today, reverse=False, *args, **kwargs):
        self.from_date = from_date
        self.till_date = till_date
        self.reverse = reverse
        super(SplitDateField, self).__init__(*args, **kwargs)

    def formfield(self, ** kwargs):
        defaults = {'form_class': SplitDateFormField, }
        defaults.update(kwargs)
        return super(SplitDateField, self).formfield(from_date=self.from_date,
            till_date=self.till_date, reverse=self.reverse, ** defaults)

try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ["^utilities\.fields\.SplitDateField"])
except ImportError:
    pass
