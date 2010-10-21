from redsolutioncms.make import BaseMake
from redsolutioncms.models import CMSSettings

class Make(BaseMake):
    def make(self):
        super(Make, self).make()
        cms_settings = CMSSettings.objects.get_settings()
        cms_settings.render_to('settings.py', 'utilities/redsolutioncms/settings.pyt')
        cms_settings.render_to('development.py', 'utilities/redsolutioncms/development.pyt')
        cms_settings.render_to(['..', 'templates', 'base_utilities.html'],
            'utilities/redsolutioncms/base_utilities.html', {
        }, 'w')
        cms_settings.base_template = 'base_utilities.html'
        cms_settings.save()

make = Make()

