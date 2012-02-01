# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.management import create_permissions
from django.db.models import get_apps


class Command(BaseCommand):
    help = 'Update permissions for all INSTALLED_APPS'

    def handle(self, *args, **options):
        for app in get_apps():
            create_permissions(app, None, 0)

