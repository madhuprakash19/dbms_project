from django.urls import path
from . import views
app_name = 'academic'

urlpatterns = [
    path('home/',views.home,name='home'),
    path('subject/',views.subject,name='teacher_subject'),
    path('view_class/<int:id>/',views.view_class,name='view_class'),
    path('markattendence/<int:class_id>/<int:attendence_id>/<int:subject_id>',views.mark_attendence,name='mark_attendence'),
    path('attendence_schedule/<int:class_id>/<int:subject_id>',views.attendence_schedules,name='attendence_schedule'),
    path('attedence/save_attendence/',views.save_attendence,name='save_attendence'),
    path('edit-view-attedence/<int:attendence_id>/<int:class_id>/<int:subject_id>/',views.edit_attendence,name='edit_attendence'),
    path('marks_list/<int:class_id>/<int:subject_id>/',views.marks_list,name='marks_list'),
    path('enter_marks/<int:class_id>/<int:subject_id>/<int:exam_id>',views.enter_marks,name='enter_marks'),
    path('edit_marks/<int:class_id>/<int:subject_id>/<int:exam_id>/<int:test_id>',views.edit_marks,name='edit_marks'),
    path('save_marks/',views.save_marks,name='save_marks'),
    path('marks_report/',views.marks_report,name='marks_report'),
    path('time/',views.time_test,name='bootstrap'),
    path('time_list/',views.time_list,name='time_list'),
    path('choose_section/<int:id>/<int:sem>',views.choose_section,name='choose_section'),
    path('select_days/<int:id>',views.select_days,name='select_days'),
    path('add_time/<int:class_id>/<int:day_id>/<int:errornum>',views.add_time,name='add_time'),
    path('save_time/',views.save_time,name='save_time'),
    path('edit_time/<int:id>',views.edit_time,name='edit_time'),
    path('delete_time/<int:id>',views.delete_time,name='delete_time'),
    path('forbidden/',views.forbidden,name='forbidden'),
]
