from django.shortcuts import render,get_object_or_404,get_list_or_404
from django.contrib.auth.decorators import login_required
from academic.models import faculty_handled_class,sub_class,registered_students,main_class,class_subject
from .forms import AttendenceForm
from django.http import HttpResponseRedirect
from django.urls import reverse
# Create your views here.
@login_required
def subject(request):
    subject = list(faculty_handled_class.objects.filter(faculty_id=request.user))

    return render(request,'subject.html',{'subject':subject})

def view_class(request,id):
    sclass = sub_class.objects.get(id=id)
    fsubjects = list(faculty_handled_class.objects.filter(faculty_id=request.user,sub_class_id=sclass))
    mclass = main_class.objects.get(id=sclass.parent_class.id)
    subjects = list(class_subject.objects.filter(class_id=mclass))
    student_list = list(registered_students.objects.filter(class_id=sclass).order_by('student'))
    return render(request,'view_class.html',{'student_list':student_list,'sclass':sclass,'subjects':subjects,'fsubjects':fsubjects})

def mark_attendence(request,class_id,attendence_id):
    sclass = sub_class.objects.get(id=class_id)
    return render(request,'mark_attendence.html',{'sclass':sclass})

def attendence_schedule(request,class_id,subject_id):
    if request.method == 'POST':
        attendence_form = AttendenceForm(data = request.POST)

        if attendence_form.is_valid():
            a = attendence_form.save(commit=False)
            a.sclass = sub_class.objects.get(id=class_id)
            a.subject = faculty_handled_class.objects.get(id=subject_id)
            a.save()
            attendence_id = a.id
            print(attendence_id)
            print(class_id)
            return HttpResponseRedirect(reverse('academic:mark_attendence',args=[class_id,attendence_id]))

    else:
        attendence_form = AttendenceForm()

    return render(request,'attendence_schedule.html',{'attendence_form':attendence_form})
