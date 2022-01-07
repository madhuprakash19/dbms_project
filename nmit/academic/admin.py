from django.contrib import admin
from . import models

admin.site.register(models.subject)
# admin.site.register(models.subject_student_enrollment)
# admin.site.register(models.subject_handler)
# admin.site.register(models.student_class)
# admin.site.register(models.class_member)
admin.site.register(models.main_class)
admin.site.register(models.sub_class)
admin.site.register(models.class_subject)
admin.site.register(models.registered_students)
admin.site.register(models.faculty_handled_class)
