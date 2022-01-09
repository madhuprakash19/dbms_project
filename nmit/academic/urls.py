from django.urls import path
from . import views
app_name = 'academic'

urlpatterns = [
    path('subject/',views.subject,name='teacher_subject'),
    path('view_class/<int:id>/',views.view_class,name='view_class'),
    path('markattendence/<int:class_id>/<int:attendence_id>/<int:subject_id>',views.mark_attendence,name='mark_attendence'),
    path('attendence_schedule/<int:class_id>/<int:subject_id>',views.attendence_schedules,name='attendence_schedule'),
    path('attedence/save_attendence/',views.save_attendence,name='save_attendence'),
]
