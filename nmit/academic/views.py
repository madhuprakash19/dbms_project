from django.shortcuts import render,get_object_or_404,get_list_or_404
from django.contrib.auth.decorators import login_required
from academic.models import (test,marks,test_type,
                            attendence_count,faculty_handled_class,
                            sub_class,registered_students,main_class,
                            class_subject,attendence_schedule,attendence)
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

    return render(request,'attendence_schedule.html',{'attendence_form':attendence_form,'attendence_list':attendence_list,'id_class':class_id,'id_subject':subject_id})


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

def edit_attendence(request,attendence_id,class_id,subject_id):
    student_list = list(attendence.objects.filter(subject__id = attendence_id))
    return render(request,'edit_attendence.html',{'attendence_id':attendence_id,'class_id':class_id,'student_list':student_list,'subject_id':subject_id})


def marks_list(request,class_id,subject_id):
    test_dict = {'LA1':'1','LA2':'2','MSE1':'3','MSE2':'4','MSE3':'5','SEE':'6'}
    a = list(test.objects.filter(subject_handler__id = subject_id))
    for i in a:
        del test_dict[i.test_type.code]


    return render(request,'marks_list.html',{'class_id':class_id,'subject_id':subject_id,'test_dict':test_dict,'a':a})

#subject_id is actually subject_handler id
def enter_marks(request,class_id,subject_id,exam_id):
    sclass = sub_class.objects.get(id=class_id)
    return render(request,'enter_marks.html',{'sclass':sclass,'class_id':class_id,'subject_id':subject_id,'exam_id':exam_id})

def edit_marks(request,class_id,subject_id,exam_id,test_id):
    sclass = sub_class.objects.get(id=class_id)
    students_marked = list(marks.objects.filter(test_id__id=test_id))
    return render(request,'edit_marks.html',{'students_marked':students_marked,'class_id':class_id,'subject_id':subject_id,'exam_id':exam_id})

def save_marks(request):
    class_id = request.POST['class_id']
    sclass = sub_class.objects.get(id = class_id)
    subject_id = request.POST['subject_id']
    faculty = faculty_handled_class.objects.get(id = subject_id)
    subject = class_subject.objects.get(id=faculty.subject.id)
    print(subject)
    test_type_object = test_type.objects.get(id = request.POST['exam_id'])

    try:
        x = test.objects.get(subject_handler=faculty,class_id=sclass,test_type=test_type_object,subject_id=subject)
    except test.DoesNotExist:
        x = test(subject_handler=faculty,class_id=sclass,test_type=test_type_object,subject_id=subject)
        x.save()

    b=[]
    for i in sclass.students.all():
        b.append(i.username)

    for i,j in request.POST.items():
        if i in b:
            if j == '':
                score = 0
            else:
                score = j
            stud = get_object_or_404(User,username = i)
            try:
                a = marks.objects.get(test_id=x,student = stud )
                a.marks_obtained = score
                a.save()
            except marks.DoesNotExist:
                a = marks(test_id=x,student = stud,marks_obtained=score)
                a.save()
    return HttpResponseRedirect(reverse('academic:marks_list',args=[class_id,subject_id]))


def marks_report(request):
    class_id = registered_students.objects.get(student=request.user)
    sclass = sub_class.objects.get(id = class_id.class_id.id)
    mclass = main_class.objects.get(id = sclass.parent_class.id)
    smarks = list(marks.objects.filter(student=request.user))
    subjects = list(class_subject.objects.filter(class_id=mclass))
    report = {}
    for i in subjects:
        report[i.class_subject.name] = {'LA1':0,'LA2':0,'MSE1':0,'MSE2':0,'MSE3':0,'SEE':0}
    for i in smarks:
        report[i.test_id.subject_id.class_subject.name][i.test_id.test_type.code] = i.marks_obtained
    print(report)
    return render(request,'marks_report.html',{'report':report})

def bootstrap_test(request):

    return render(request,'bootstrap_test.html')














    #
