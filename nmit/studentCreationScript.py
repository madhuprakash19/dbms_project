from django.contrib.auth.models import User
from user.models import user_profile,user_status,role
from info.models import student_details,hostel,department
from academic.models import main_class,sub_class,registered_students

import csv

results = []
with open("input.csv") as csvfile:
    reader = csv.reader(csvfile, quoting=csv.QUOTE_NONNUMERIC)
    for row in reader:
        results.append(row)

print(results)

try:
    user=User.objects.create_user('test1', password='test1')
    user.save()
    print("test1 created")
except:
    print("User already Exists")
username = User.objects.get(username='test1')
status=user_status.objects.get(id=1)
role_status=role.objects.get(id=1)


try:
    temp = user_profile.objects.get(user=username)
    print("User profile already Exists")
except:
    profile = user_profile(user=username,role_id=role_status,user_status=status)
    profile.save()
    print("test1 user profile created")

dept = department.objects.get(id=1)
sname = "test1"
susn = '1NT19IS185'

try:
    temp =  student_details.objects.get(user=username)
    temp.name = sname
    temp.usn = susn
    temp.dept_id = dept
    temp.save()
    print("User updated")
except:
    student = student_details(user=username,name=sname,usn=susn,dept_id=dept)
    student.save()
    print("student_details created")

try:
    main_class = main_class.objects.get(sem='7',dept_id=dept)
except:
    temp=main_class(sem='7',dept_id=dept)
    temp.save()
    main_class = main_class.objects.get(sem='7',dept_id=dept)
    print("Main class not found. Created New one")

print(main_class)

try:
    sub_class = sub_class.objects.get(parent_class=main_class,section='C')
except:
    temp = sub_class(parent_class=main_class,section='C')
    temp.save()
    sub_class = sub_class.objects.get(parent_class=main_class,section='C')
    print("Sub class not found. Created New one")

print(sub_class)

try:
    temp = registered_students.objects.get(class_id=sub_class,student=username)
    print("User already taken the course")
except:
    registration = registered_students(class_id=sub_class,student=username)
    registration.save()
    print("student sucessfully registered")
