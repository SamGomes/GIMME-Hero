
from django.contrib import admin
from django.db import models
from django.forms import TextInput, Textarea

from GIMMEWeb.core.models import *


class GeneralAdmin(admin.ModelAdmin):
	formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'100%'})},
        models.TextField: {'widget': Textarea(attrs={'rows':4, 'cols':100})},
    }
# admin.site.register(User,GeneralAdmin)
admin.site.register(UserProfile,GeneralAdmin)
admin.site.register(Task,GeneralAdmin)