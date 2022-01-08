from django.contrib.auth.models import User
from user.models import user_profile,user_status,role
from info.models import student_details,hostel,department
from academic.models import main_class,sub_class,registered_students

# exec(open("studentCreationScript.py").read())-->to run from shell

import json
import time

f = open('student.json')
data = json.load(f)

n = len(data)

for i in range(0,n):
    print("Number "+str(i))

    try:
        user=User.objects.create_user(data[i]['USN'], password=data[i]['USN'])
        user.save()
        print(data[i]['USN']+" created")
    except:
        print(data[i]['USN']+" already Exists")

    username = User.objects.get(username=data[i]['USN'])
    status=user_status.objects.get(id=1)
    role_status=role.objects.get(id=1)

    try:
        username.first_name = data[i]['NAME']
        username.save()
    except:
        print('Sorry that cant be done')


    try:
        temp = user_profile.objects.get(user=username)
        print(data[i]['USN']+" profile already Exists")
    except:
        profile = user_profile(user=username,role_id=role_status,user_status=status)
        profile.save()
        print(data[i]['USN']+" user profile created")


    dept = department.objects.get(id=data[i]['BRANCH'])
    sname = data[i]['NAME']
    susn = data[i]['USN']

    try:
        temp =  student_details.objects.get(user=username)
        temp.name = sname
        temp.usn = susn
        temp.dept_id = dept
        temp.save()
        print(sname+" details updated")
    except:
        student = student_details(user=username,name=sname,usn=susn,dept_id=dept)
        student.save()
        print(sname+" details created")
    # print(data[i]['SEM'])
    # print(dept)
    try:
        print("in try")
        main_classes = main_class.objects.get(sem=str(data[i]['SEM']),dept_id=dept)
    except:
        print("in exception")
        temp = main_class(sem=data[i]['SEM'],dept_id=dept)
        temp.save()
        main_classes = main_class.objects.get(sem=data[i]['SEM'],dept_id=dept)
        print("Main class not found. Created New one")

    print(main_classes)

    try:
        sub_classes = sub_class.objects.get(parent_class=main_classes,section=data[i]['SECTION'])
    except:
        temp = sub_class(parent_class=main_classes,section=data[i]['SECTION'])
        temp.save()
        sub_classes = sub_class.objects.get(parent_class=main_classes,section=data[i]['SECTION'])
        print("Sub class not found. Created New one")

    print(sub_classes)

    try:
        temp = registered_students.objects.get(class_id=sub_classes,student=username)
        print("User already taken the course")
    except:
        registration = registered_students(class_id=sub_classes,student=username)
        registration.save()
        print("student sucessfully registered")
