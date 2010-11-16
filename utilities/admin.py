# -*- coding: utf-8 -*-
from django import forms
from django.contrib import admin
from django.contrib.sessions.models import Session
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import UserChangeForm, PasswordResetForm
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from utilities.settings import ALLOW_DOT_IS_USERNAME, ENABLE_PASSWORD_RESET
from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import ugettext, ugettext_lazy as _
from django.shortcuts import render_to_response, get_object_or_404
from django.utils.html import escape
from django.template import RequestContext
try:
    from django.contrib import messages
except ImportError:
    pass

class MoidfiedPasswordResetForm(PasswordResetForm):

    def clean_email(self):
        """
        Validates that a user exists with the given e-mail address.
        Closes Django ticket #14674 http://code.djangoproject.com/ticket/14674
        Also resets all user's sesions and sets unusable password for user
        """
        from django.contrib.auth.models import UNUSABLE_PASSWORD
        email = self.cleaned_data["email"]
        self.users_cache = User.objects.filter(email__iexact=email).exclude(
            password=UNUSABLE_PASSWORD)
        if len(self.users_cache) == 0:
            raise forms.ValidationError(_("That e-mail address doesn't have an associated user account. Are you sure you've registered?"))
        return email

    def save(self, *args, **kwds):
        # Now clear user's sessions:
        for session in Session.objects.all():
            for user in self.users_cache:
                user.set_unusable_password()
                user.save()
                if session.get_decoded().get('_auth_user_id') == user.id:
                    session.delete()

        super(MoidfiedPasswordResetForm, self).save(*args, **kwds)

class ModifiedUserChangeForm(UserChangeForm):
    email = forms.EmailField(label=_("E-mail"), max_length=75,
        help_text=_('<a href="%s">Reset password</a> for this user.' % 'reset/'),
        required=False)

class ResetPasswordMixin(object):
    '''
        Mixin adds reset password link to user change form in admin site.
        Added view with ResetPasswordForm, user will set temporary password
        and recieve email with reset password link. 
    '''

    def __init__(self, *args, **kwds):
        super(ResetPasswordMixin, self).__init__(*args, **kwds)
        self.form = ModifiedUserChangeForm


    def get_urls(self):
        from django.conf.urls.defaults import patterns
        return patterns('',
            (r'^(\d+)/reset/$', self.admin_site.admin_view(self.reset_password))
        ) + super(ResetPasswordMixin, self).get_urls()

    def reset_password(self, request, id):
        '''
        Almost copied from ``django.contrb.auth.admin.UserAdmin.user_change_password``
        Resets user password to teporary value, send email to user with reset-password link.
        '''
        if not self.has_change_permission(request):
            raise PermissionDenied
        user = get_object_or_404(self.model, pk=id)
        if request.method == 'POST':
            form = MoidfiedPasswordResetForm(request.POST)
            if form.is_valid():
                new_user = form.save()
                try:
                    msg = ugettext('Password for user %s has been reseted.' % user)
                    messages.success(request, msg)
                except NameError:
                    # there's no messages framework in Django 1.1
                    pass
                return HttpResponseRedirect('..')
        else:
            msg = ugettext('Password for user %s has been reseted.' % user)
            form = MoidfiedPasswordResetForm({'email': user.email})

        fieldsets = [(None, {'fields': form.base_fields.keys()})]
        adminForm = admin.helpers.AdminForm(form, fieldsets, {})

        return render_to_response(self.change_user_password_template or 'admin/reset_password.html', {
            'title': _('Reset password: %s') % escape(user.username),
            'adminForm': adminForm,
            'form': form,
            'is_popup': '_popup' in request.REQUEST,
            'add': True,
            'change': False,
            'has_delete_permission': False,
            'has_change_permission': True,
            'has_absolute_url': False,
            'opts': self.model._meta,
            'original': user,
            'save_as': False,
            'show_save': True,
            'root_path': self.admin_site.root_path,
        }, context_instance=RequestContext(request))


if ENABLE_PASSWORD_RESET:
    UserAdminClass = admin.site._registry[User].__class__

    class NewClass(ResetPasswordMixin, UserAdminClass):
        pass

    try:
        admin.site.unregister(User)
    except admin.sites.NotRegistered:
        raise ImproperlyConfigured("Can not found User admin. Check if 'utilities' inserted in INSTALLED_APPS *after* 'django.contrib.auth'")

    admin.site.register(User, NewClass)
