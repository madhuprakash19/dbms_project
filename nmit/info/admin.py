from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.hostel)
admin.site.register(models.department)
admin.site.register(models.designation)
admin.site.register(models.faculty)
admin.site.register(models.student_details)
admin.site.register(models.student_hostel)
