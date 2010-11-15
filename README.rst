================
django-utilities
================

A set of Django useful utilities.

* ImageField with preview in admin interface
* Override allows to create users with dot in username
* Localized date filter
* ConsoleException middleware

Installation:
=============

1. Put ``utilities`` in to your ``INSTALLED_APPS`` in your ``settings.py`` within your django project.

Usage:
======

ImagePreviewField:
------------------

Used to show image preview near ImageField.

To use it in your ``models.py`` ::

	from utilities.fields import ImagePreviewFieldd

	class MyModel(models.Model):
		image = ImagePreviewField(upload_to='upload/')

You can specify maximum width and height for the thumb ::

	class MyModel(models.Model):
		image = ImagePreviewField(upload_to='upload/', thumb_size=(80, 80))


If you have separated field with thumb for this image you can specify its name and told to use its real size::

	class MyModel(models.Model):
		thumb = models.ImageField(upload_to='thumb/')
		image = ImagePreviewField(upload_to='upload/', thumb_field='thumb', thumb_size=None)

Dot is username:
----------------

By default this application will allow you to create users in admin with dot in there names.
To disallow set ``ALLOW_DOT_IS_USERNAME`` to ``False`` in your ``settings.py``.  


Local date template filter:
---------------------------

The ``date_local`` filter supposed to be used with Django 1.1 (1.2+ already has such feature ).
Load filter with ``{% load utilities_tags %}`` and use it like date `Django date filter`_ 

For example: ::

	{{ entry.creation_date|date_local:"d F Y" }}

Returns 01 Января 2010 for ``ru`` locale

ConsoleException middleware:
----------------------------

Often you get annoyed when Django show Tracebacks like ::
    
    File "/home/mysite/django-mysite3/django/template/__init__.py", line
    800, in render_node
    return node.render(context)

ConsoleException middleware prints original tracebacks in STDOUT. It is very helpful
for debugging sometimes. 
Use it **ONLY** in development mode!

Reset password form:
--------------------

To enable password reset form, set in your ``settings.py``::

    ENABLE_PASSWORD_RESET = True

You will get  link to password reset in users administration section under email
field.
When you reset password to some user,  all his or her active sessions will be 
deleted, password will be set to unusable.
The only way to login is follow link, provided in email.
If user has no email, you will not able reset password for this user.

Classifiers:
-------------

`Utilities`_

.. _`Django date filter`: http://docs.djangoproject.com/en/1.1/ref/templates/builtins/#now
.. _`Utilities`: http://www.redsolutioncms.org/classifiers/utilities