from django.contrib import admin
from . import models

admin.site.register(models.subject)
admin.site.register(models.subject_student_enrollment)
admin.site.register(models.subject_handler)
admin.site.register(models.student_class)
admin.site.register(models.class_member)
