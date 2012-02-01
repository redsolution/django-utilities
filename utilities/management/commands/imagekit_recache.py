# -*- coding: utf-8 -*-
from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from django.db.models import loading
from shutil import rmtree
from django.conf import settings
from os.path import join
import sys

def progressbar(it, prefix = "", size = 60):
    count = len(it)
    def _show(_i):
        x = int(size*_i/count)
        sys.stdout.write("%s[%s%s] %i/%i\r" % (prefix, "#"*x, "."*(size-x), _i, count))
        sys.stdout.flush()

    _show(0)
    for i, item in enumerate(it):
        yield item
        _show(i+1)
    sys.stdout.write("\n")
    sys.stdout.flush()


class Command(BaseCommand):
    args = 'applabel.Model'
    help = '''Regeneartes djnago-imagekit cached images.
    Usage: manage.py imagekit_gencache attachment.AttachemntImage [--force]
    '''
    option_list = BaseCommand.option_list + (
        make_option('--force',
            action='store_true',
            dest='force',
            default=False,
            help='Force delete cache directory'),
    )

    def handle(self, *args, **options):
        app_label, model_name =args[0].split('.')
        model_cls = loading.get_model(app_label, model_name)
        ikspecs = model_cls._ik.specs
        
        if options['force']:
            # Delete cache dir
            print 'Forced remove previous cache dir: ', model_cls._ik.cache_dir,
            try:
                rmtree(join(settings.MEDIA_ROOT, model_cls._ik.cache_dir), ignore_errors=False)
            except (IOError, OSError):
                print '[Fail]'
            else:
                print '[OK]'

        for spec in ikspecs:
            for instance in progressbar(model_cls.objects.all(), "Pre-caching %s: " % spec.name(), 80):
                img = getattr(instance, spec.name())
                getattr(img, 'url')
