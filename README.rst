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

And include utilities urls into your urlconf::

    urlpatterns += patterns('',
        (r'^', include('utilities.urls')),
    )

You will get  link to password reset in users administration section under email
field.
When you reset password to some user,  all his or her active sessions will be 
deleted, password will be set to unusable.
The only way to login is follow link, provided in email.
If user has no email, you will not able reset password for this user.

SplitDateField:
---------------

You can specify minimal and maximum date with attributes ``from_date`` (default
``datetime.date(1930,01,01)``) and ``till_date`` (default ``datetime.date.today``)
, they must have date type or be callable object. Also you may reverse order of 
years with help of boolean attribute ``reverse`` (default False).

If ``from_date=datetime.date(2007,01,01)``, ``till_date=datetime.date(2010,01,01)`` 
and ``reverse=False``, then we obtain the sequence of years: 2007, 2008, 2009, 2010

To use it in your ``models.py`` ::

  from utilities.fields import SplitDateField
  
    class MyModel(models.Model):
      date = SplitDateField(from_date=datetime.date(2008,10,01),
        till_date=datetime.date.today, reverse=True)
        
To use  it in your ``forms.py`` ::

  from utilities.fields import SplitDateFormField
  
    class MyForm(forms.Form)
      date = SplitDateFormField(from_date=datetime.date(2008,10,01),
        till_date=datetime.date.today, reverse=True)


Management commands:
--------------------

Since 0.1.4 few management commands added:

**imagekit_recache**
  Re-create cache for imagekit models. Command has --force option to delete old cache dir.

**update_permissions**
  Update permissions for installed models. Useful if you change permissions in project's lifecycle.


Classifiers:
-------------

`Utilities`_

.. _`Django date filter`: http://docs.djangoproject.com/en/1.1/ref/templates/builtins/#now
.. _`Utilities`: http://www.redsolutioncms.org/classifiers/utilities


History:
--------

0.1.0 (2010-11-04)
```````````````````
* Initial release

0.1.1 (2010-11-15)
``````````````````

* Aded reset password form

0.1.2 (2010-11-16)
``````````````````

* Bugfixes in ``date_local`` template filter
* Fixed compability ``ResetPasswordForm`` in Django 1.1

0.1.3 (2010-11-23)
``````````````````

* Add ``SplitDateField``

0.1.4 (2012-02-01)
```````````````````

* Added management commands, wrapped ImagePreviewField IOError

