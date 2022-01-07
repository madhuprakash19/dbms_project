from django.urls import path
from . import views
app_name = 'academic'

urlpatterns = [
    path('subject/',views.subject,name='teacher_subject'),
    path('view_class/<int:id>/',views.view_class,name='view_class'),
]
