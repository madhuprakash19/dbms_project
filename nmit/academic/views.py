from django.shortcuts import render,get_object_or_404,get_list_or_404
from django.contrib.auth.decorators import login_required
from academic.models import faculty_handled_class,sub_class,registered_students,main_class,class_subject

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

def mark_attendence(request,class_id,subject_id):
    sclass = sub_class.objects.get(id=class_id)
    return render(request,'mark_attendence.html',{'sclass':sclass})
