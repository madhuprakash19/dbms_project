from django.contrib import admin
from . import models
# Register your models here.

admin.site.register(models.user_status)
admin.site.register(models.role)
admin.site.register(models.user_profile)
#admin.site.register(models.user_model)
