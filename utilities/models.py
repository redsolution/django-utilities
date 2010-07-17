import re
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from utilities.settings import ALLOW_DOT_IS_USERNAME

if ALLOW_DOT_IS_USERNAME:
    UserCreationForm.base_fields['username'].regex = re.compile(r'^[-\.\w]+$')
    UserChangeForm.base_fields['username'].regex = re.compile(r'^[-\.\w]+$')
