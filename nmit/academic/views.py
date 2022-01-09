from django.shortcuts import render,get_object_or_404,get_list_or_404
from django.contrib.auth.decorators import login_required
from academic.models import attendence_count,faculty_handled_class,sub_class,registered_students,main_class,class_subject,attendence_schedule,attendence
from .forms import AttendenceForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
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

    a={}
    for i in subjects:
        a[i.class_subject]={'class_id':0,'subject_id':0}
    for i in fsubjects:
        a[i.subject.class_subject]['class_id']=sclass.id
        a[i.subject.class_subject]['subject_id']=i.id
    print(a)


    return render(request,'view_class.html',{'student_list':student_list,'sclass':sclass,'a':a})

def mark_attendence(request,class_id,attendence_id,subject_id):
    sclass = sub_class.objects.get(id=class_id)
    return render(request,'mark_attendence.html',{'sclass':sclass,'attendence_id':attendence_id,'subject_id':subject_id,'class_id':class_id})

def attendence_schedules(request,class_id,subject_id):
    attendence_list = list(attendence_schedule.objects.filter(subject__id=subject_id).order_by('-id')) #double __ is used to point the id of the pointing foreign key object
    if request.method == 'POST':
        attendence_form = AttendenceForm(data = request.POST)

        if attendence_form.is_valid():
            a = attendence_form.save(commit=False)
            a.sclass = sub_class.objects.get(id=class_id)
            a.subject = faculty_handled_class.objects.get(id=subject_id)
            a.save()
            attendence_id = a.id
            return HttpResponseRedirect(reverse('academic:mark_attendence',args=[class_id,attendence_id,subject_id]))

    else:
        attendence_form = AttendenceForm()

    return render(request,'attendence_schedule.html',{'attendence_form':attendence_form,'attendence_list':attendence_list})


def save_attendence(request):
    attendence_list = attendence_schedule.objects.get(id=request.POST['attendence_id'])
    class_id = request.POST['class_id']
    subject_id = request.POST['subject_id']
    subject = faculty_handled_class.objects.get(id=subject_id)
    sclass = sub_class.objects.get(id=class_id)
    b=[]
    for i in sclass.students.all():
        b.append(i.username)
    for i,j in request.POST.items():
        if i in b:
            status = j
            if status == 'present':
                status = True
            else:
                status = False
            stud = get_object_or_404(User,username = i)
            if attendence_list.status == True:
                try:
                    a = attendence.objects.get(subject=attendence_list,student = stud )
                    count_edit(a,status,subject,stud,sclass)
                    a.status = status
                    a.save()
                except attendence.DoesNotExist:
                    a = attendence(subject=attendence_list,student = stud,status = status)
                    a.save()
                    count_add(status,subject,stud,sclass)
            else:
                a = attendence(subject=attendence_list,student = stud ,status = status)
                a.save()
                attendence_list.status = True
                attendence_list.save()
                count_add(status,subject,stud,sclass)
    return HttpResponseRedirect(reverse('academic:attendence_schedule',args=[class_id,subject_id]))


def count_edit(old,new,subject,student,sclass):
    if old.status==False and new==True:
        try:
            acount = attendence_count.objects.get(subject=subject,student=student)
            acount.attended_class += 1
            acount.save()
        except:
            acount = attendence_count(subject=subject,student=student,sclass=sclass)
            acount.save()
            acount.total_class +=1
            acount.attended_class += 1
            acount.save()
    elif old.status==True and new==False:
        try:
            acount = attendence_count.objects.get(subject=subject,student=student)
            acount.attended_class -= 1
            acount.save()
        except:
            acount = attendence_count(subject=subject,student=student,sclass=sclass)
            acount.save()
            acount.total_class +=1
            acount.save()

def count_add(new,subject,student,sclass):
    if new:
        try:
            acount = attendence_count.objects.get(subject=subject,student=student)
            acount.attended_class += 1
            acount.total_class +=1
            acount.save()
        except:
            acount = attendence_count(subject=subject,student=student,sclass=sclass)
            acount.save()
            acount.total_class +=1
            acount.attended_class += 1
            acount.save()
    else:
        try:
            acount = attendence_count.objects.get(subject=subject,student=student)
            acount.total_class +=1
            acount.save()
        except:
            acount = attendence_count(subject=subject,student=student,sclass=sclass)
            acount.save()
            acount.total_class +=1
            acount.save()































#
