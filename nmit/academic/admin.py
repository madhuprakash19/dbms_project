from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.subject)
admin.site.register(models.subject_student_enrollment)
admin.site.register(models.subject_handler)
admin.site.register(models.class)
admin.site.register(models.class_member)
