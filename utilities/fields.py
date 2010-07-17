# -*- coding: utf-8 -*-

from django import forms
from django.db import models
from django.contrib.admin.widgets import AdminFileWidget
from utilities.widgets import ImagePreviewWidget

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
