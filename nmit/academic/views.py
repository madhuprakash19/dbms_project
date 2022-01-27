from django.shortcuts import render,get_object_or_404,get_list_or_404
from django.contrib.auth.decorators import login_required
from academic.models import (test,marks,test_type,
                            attendence_count,faculty_handled_class,
                            sub_class,registered_students,main_class,
                            class_subject,attendence_schedule,attendence,
                            time_table,days)
from info.models import teacher,department
from user.models import user_profile
from .forms import AttendenceForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User

from datetime import datetime
# Create your views here.
def forbidden(request):
    return render(request,'403.html')

@login_required()
def home(request):
    today = datetime.today().strftime('%A')
    if(student_status(request.user)):
        try:
            day_subject = registered_students.objects.get(student=request.user)
            sclass = day_subject.class_id
            day = days.objects.get(name = today)
            day_subject = list(time_table.objects.filter(sclass = sclass,day = day))
        except:
            day_subject = 'There are no classes today'
        return render(request,'student_home.html',{'day_subject':day_subject})
    elif(hod_status(request.user)):
        day = days.objects.get(name = today)
        try:
            day_subject = list(time_table.objects.filter(day = day,teacher=request.user))
        except:
            day_subject = 'There are no classes today'
        return render(request,'hod_home.html',{'day':day,'day_subject':day_subject})
    elif(faculty_status(request.user)):
        day = days.objects.get(name = today)
        try:
            day_subject = list(time_table.objects.filter(day = day,teacher=request.user))
        except:
            day_subject = 'There are no classes today'
        return render(request,'faculty_home.html',{'day':day,'day_subject':day_subject})

    return render(request,'home.html',{'day':day})




@login_required
def subject(request):
    if(faculty_status(request.user)):
        subject = list(faculty_handled_class.objects.filter(faculty_id=request.user))
        return render(request,'subject.html',{'subject':subject})
    else:
        return forbidden(request)

@login_required
def view_class(request,id):
    if(faculty_status(request.user)):
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


        return render(request,'view_class.html',{'student_list':student_list,'sclass':sclass,'a':a})
    else:
        return forbidden(request)

@login_required
def mark_attendence(request,class_id,attendence_id,subject_id):
    if(faculty_status(request.user)):
        sclass = sub_class.objects.get(id=class_id)
        return render(request,'mark_attendence.html',{'sclass':sclass,'attendence_id':attendence_id,'subject_id':subject_id,'class_id':class_id})
    else:
        return forbidden(request)

@login_required
def attendence_schedules(request,class_id,subject_id):
    if(faculty_status(request.user)):
        sclass = sub_class.objects.get(id=class_id)
        subject = faculty_handled_class.objects.get(id=subject_id)
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

        return render(request,'attendence_schedule.html',{'attendence_form':attendence_form,'attendence_list':attendence_list,'id_class':class_id,'id_subject':subject_id,'sclass':sclass,'subject':subject})
    else:
        return forbidden(request)

@login_required
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

@login_required
def edit_attendence(request,attendence_id,class_id,subject_id):
    if(faculty_status(request.user)):
        student_list = list(attendence.objects.filter(subject__id = attendence_id))
        return render(request,'edit_attendence.html',{'attendence_id':attendence_id,'class_id':class_id,'student_list':student_list,'subject_id':subject_id})
    else:
        return forbidden(request)


@login_required
def marks_list(request,class_id,subject_id):
    if(faculty_status(request.user)):
        sclass = sub_class.objects.get(id=class_id)
        test_dict = {'LA1':'1','LA2':'2','MSE1':'3','MSE2':'4','MSE3':'5','SEE':'6'}
        a = list(test.objects.filter(subject_handler__id = subject_id))
        for i in a:
            del test_dict[i.test_type.code]


        return render(request,'marks_list.html',{'class_id':class_id,'subject_id':subject_id,'test_dict':test_dict,'a':a,'sclass':sclass})
    else:
        return forbidden(request)

#subject_id is actually subject_handler id
@login_required
def enter_marks(request,class_id,subject_id,exam_id):
    if(faculty_status(request.user)):
        sclass = sub_class.objects.get(id=class_id)
        return render(request,'enter_marks.html',{'sclass':sclass,'class_id':class_id,'subject_id':subject_id,'exam_id':exam_id})
    else:
        return forbidden(request)

@login_required
def edit_marks(request,class_id,subject_id,exam_id,test_id):
    if(faculty_status(request.user)):
        sclass = sub_class.objects.get(id=class_id)
        students_marked = list(marks.objects.filter(test_id__id=test_id))
        return render(request,'edit_marks.html',{'students_marked':students_marked,'class_id':class_id,'subject_id':subject_id,'exam_id':exam_id})
    else:
        return forbidden(request)


@login_required
def save_marks(request):
    class_id = request.POST['class_id']
    sclass = sub_class.objects.get(id = class_id)
    subject_id = request.POST['subject_id']
    faculty = faculty_handled_class.objects.get(id = subject_id)
    subject = class_subject.objects.get(id=faculty.subject.id)
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


@login_required
def marks_report(request):
    if(student_status(request.user)):
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
        return render(request,'marks_report.html',{'report':report})
    else:
        return forbidden(request)

@login_required
def time_test(request):
    return render(request,'time.html')


def hod_status(user):
    try:
        hod_status = teacher.objects.get(user=user)
        if hod_status.designation_id.id == 2:
            return True
        else:
            return False
    except:
        return False

def faculty_status(user):
    teacher = user_profile.objects.get(user=user)
    if teacher.role_id.id == 2:
        return True
    else:
        return False

def student_status(user):
    student = user_profile.objects.get(user=user)
    if student.role_id.id == 1:
        return True
    else:
        return False



@login_required
def time_list(request):
    error=''
    a=[]
    try:
        hod_status = teacher.objects.get(user=request.user)
        if hod_status.designation_id.id == 2:
            dept = department.objects.get(id = hod_status.dept_id.id)
            mclass = list(main_class.objects.filter(dept_id=dept))
        else:
            error = "You dont have permissions"
            return forbidden(request)
    except:
        error = "You dont have permissions"
        return forbidden(request)

    return render(request,'time_list.html',{'error':error,'mclass':mclass})


@login_required
def choose_section(request,id,sem):
    if(hod_status(request.user)):
        sclass = list(sub_class.objects.filter(parent_class__id = id))
        return render(request,'choose_section.html',{'sclass':sclass,'sem':sem})
    else:
        return forbidden(request)

@login_required
def select_days(request,id):
    if(hod_status(request.user)):
        unmarked_days = {1:'Monday',2:'Tuesday',3:'Wednesday',4:'Thrusday',5:'Friday',6:'Saturday'}
        return render(request,'select_days.html',{'unmarked_days':unmarked_days,'id':id})
    else:
        return forbidden(request)

@login_required
def add_time(request,class_id,day_id,errornum):
    if(hod_status(request.user)):
        if(errornum==1):
            error = "Sucess New Time table added"
        elif(errornum==2):
            error = "Sucess Time table Updated"
        elif(errornum==3):
            error = "Opps the selected Faculty has other class in the alloted time duration"
        elif(errornum==4):
            error = "Opps there is already a class exited in the alloted time slot"
        elif(errornum==5):
            error = "Delete Success"
        elif(errornum==6):
            error = "Delete Operation cancled"
        else:
            error = ''

        teacher = list(faculty_handled_class.objects.filter(sub_class_id__id = class_id))
        marked_days = list(time_table.objects.filter(sclass__id = class_id,day__id = day_id ))

        return render(request,'add_time.html',{'class_id':class_id,'day_id':day_id,'teacher':teacher,'error':error,'marked_days':marked_days})
    else:
        return forbidden(request)


@login_required
def save_time(request):
    errornum = 0
    start_time = request.POST['start_time']
    end_time = request.POST['end_time']
    day_id = request.POST['day']
    sub_id = request.POST['subjects']
    new = request.POST['new']
    class_id = request.POST['class']

    sub = faculty_handled_class.objects.get(id=sub_id)
    teachergot = User.objects.get(id = sub.faculty_id.id)
    dayobj = days.objects.get(id=day_id)
    class_sub = sub_class.objects.get(id=class_id)
    marked_days = list(time_table.objects.filter(sclass__id = class_id,day__id = day_id ))
    teacher = list(faculty_handled_class.objects.filter(sub_class_id__id = class_id))


    a = list(time_table.objects.filter(start_time__range=[start_time, end_time],day=dayobj,teacher=teachergot))
    a = a + list(time_table.objects.filter(end_time__range=[start_time, end_time],day=dayobj,teacher=teachergot))
    b = list(time_table.objects.filter(end_time__range=[start_time, end_time],sclass=class_sub,day=dayobj))
    b = b + list(time_table.objects.filter(start_time__range=[start_time, end_time],sclass=class_sub,day=dayobj))

    if len(a)>0:
        errornum = 3
        return HttpResponseRedirect(reverse('academic:add_time',args=[class_id,day_id,errornum]))
    elif len(b)>0:
        errornum = 4
        return HttpResponseRedirect(reverse('academic:add_time',args=[class_id,day_id,errornum]))
    elif new == '1' and len(a)==0 and len(b)==0:
        save_time = time_table(faculty=sub,teacher=teachergot,start_time=start_time,end_time=end_time,day=dayobj,sclass=class_sub)
        save_time.save()
        marked_days = list(time_table.objects.filter(sclass__id = class_id,day__id = day_id ))
        errornum = 1
        return HttpResponseRedirect(reverse('academic:add_time',args=[class_id,day_id,errornum]))
    elif new == '0' and len(a)==0 and len(b)==0:
        id_time = request.POST['time_id']
        save_time = time_table.objects.get(id = id_time)
        save_time.start_time = start_time
        save_time.end_time = end_time
        save_time.teacher = teachergot
        save_time.faculty = sub
        save_time.save()
        errornum = 2
        marked_days = list(time_table.objects.filter(sclass__id = class_id,day__id = day_id ))
        return HttpResponseRedirect(reverse('academic:add_time',args=[class_id,day_id,errornum]))

        return HttpResponseRedirect(reverse('academic:add_time',args=[class_id,day_id,errornum]))


@login_required
def edit_time(request,id):
    if(faculty_status(request.user)):
        error = ''
        time = time_table.objects.get(id = id)
        sclass = time.sclass
        day = time.day
        select_teacher = time.faculty.id

        teacher = list(faculty_handled_class.objects.filter(sub_class_id = sclass))
        marked_days = list(time_table.objects.filter(sclass = sclass,day = day))

        return render(request,'edit_time.html',{'teacher':teacher,'error':error,'marked_days':marked_days,'time':time,'select_teacher':select_teacher})
    else:
        return forbidden(request)

@login_required
def delete_time(request,id):
    if(faculty_status(request.user)):
        time = time_table.objects.get(id = id)
        class_id = time.sclass.id
        day_id = time.day.id

        if request.method == 'POST':
            time.delete()
            errornum = 5
            return HttpResponseRedirect(reverse('academic:add_time',args=[class_id,day_id,errornum]))


        return render(request,'delete_time.html',{'time':time})
    else:
        return forbidden(request)


@login_required
def attendence_report(request):
    if(student_status(request.user)):
        a = {}
        attend = list(attendence_count.objects.filter(student=request.user))
        for i in attend:
            a[i.subject] = {'total':0,'attended':0,'css':0,'percentage':0}
            a[i.subject]['total'] = i.total_class
            a[i.subject]['attended'] = i.attended_class
            temp = float(i.attended_class*100/i.total_class)
            temp = round(temp,2)
            a[i.subject]['percentage'] = temp
            if temp>85:
                css = 'btn btn-success'
            elif temp>65:
                css = "btn btn-warning"
            else:
                css = "btn btn-danger"
            a[i.subject]['css'] = css
        return render(request,'attendence_report.html',{'a':a})
    else:
        return forbidden(request)
