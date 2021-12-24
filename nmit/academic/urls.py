from django.urls import path
from . import views
app_name = 'academic'

urlpatterns = [
    path('subject/',views.subject,name='teacher_subject')
]
