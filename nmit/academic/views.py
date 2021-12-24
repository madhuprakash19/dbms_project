from django.shortcuts import render,get_object_or_404,get_list_or_404
from django.contrib.auth.decorators import login_required

from academic.models import subject_handler
# Create your views here.
@login_required
def subject(request):
    subject = list(subject_handler.objects.filter(faculty_id=request.user))

    print(subject)
    return render(request,'subject.html',{'subject':subject})
