from django.db import models
from info.models import department
from django.contrib.auth.models import User

class subject(models.Model):
    name = models.CharField(max_length=50,blank=True,null=True)
    code = models.CharField(max_length=10,blank=True,null=True)
    dept_id = models.ForeignKey(department,on_delete = models.CASCADE,blank=True,null=True)
    description = models.CharField(max_length=50,blank=True,null=True)
    credit = models.IntegerField(blank=True,null=True,default=3)


    def __str__(self):
        return str(self.name)+" "+str(self.code)

class main_class(models.Model):
    sem = models.CharField(max_length=50,blank=True,null=True)
    dept_id = models.ForeignKey(department,on_delete = models.CASCADE,blank=True,null=True)
    academic_year = models.CharField(max_length=50,blank=True,null=True)
    is_active = models.BooleanField(default=True)
    subjects = models.ManyToManyField(subject,through='class_subject')

    def __str__(self):
        return str("Main "+self.sem+"th sem "+self.dept_id.code)

class class_subject(models.Model):
    class_id = models.ForeignKey(main_class,on_delete = models.CASCADE,blank=True,null=True)
    class_subject = models.ForeignKey(subject,on_delete = models.CASCADE,blank=True,null=True)

    def __str__(self):
        return str(self.class_id.sem+" "+self.class_subject.name)

class sub_class(models.Model):
    parent_class = models.ForeignKey(main_class,on_delete = models.CASCADE)
    section = models.CharField(max_length=10,blank=True,null=True)
    class_teacher = models.ForeignKey(User,on_delete = models.CASCADE,blank=True,null=True,related_name='class_teacher')
    is_active = models.BooleanField(default=True)
    students = models.ManyToManyField(User,through='registered_students')

    def __str__(self):
        return str(self.parent_class.sem+" "+self.section+" "+self.parent_class.dept_id.code)

class registered_students(models.Model):
    class_id = models.ForeignKey(sub_class,on_delete = models.CASCADE,blank=True,null=True)
    student = models.ForeignKey(User,on_delete = models.CASCADE,blank=True,null=True)

    def __str__(self):
        return str(self.student.username)

class faculty_handled_class(models.Model):
    faculty_id =  models.ForeignKey(User,on_delete = models.CASCADE,blank=True,null=True)
    subject = models.ForeignKey(class_subject,on_delete = models.CASCADE)
    sub_class_id = models.ForeignKey(sub_class,on_delete = models.CASCADE)

    def __str__(self):
        return str(self.faculty_id)+" "+str(self.subject)



# class student_class(models.Model):
#     sem = models.CharField(max_length=10,blank=True,null=True)
#     section = models.CharField(max_length=10,blank=True,null=True)
#     dept_id = models.ForeignKey(department,on_delete = models.CASCADE,blank=True,null=True)
#     academic_year = models.IntegerField(blank=True,null=True)
#     students = models.ManyToManyField(User,through='class_member')
#     is_active = models.BooleanField(blank=True,null=True)
#
#     def __str__(self):
#         return str(self.sem)+" "+self.section

# class subject_student_enrollment(models.Model):
#     student = models.ForeignKey(User,related_name='adm_no',on_delete = models.CASCADE,blank=True,null=True)
#     subject_id = models.ForeignKey(subject,on_delete = models.CASCADE,blank=True,null=True)
#
#     def __str__(self):
#         return str(self.id)
#
# class subject_handler(models.Model):
#     subject_id = models.ForeignKey(subject,on_delete = models.CASCADE,blank=True,null=True)
#     faculty_id = models.ForeignKey(User,on_delete = models.CASCADE,blank=True,null=True)
#     class_id = models.ForeignKey(student_class,related_name='clas_id',on_delete = models.CASCADE,blank=True,null=True)
#     is_active = models.BooleanField()
#
#     def __str__(self):
#         return str(self.id)
#
# class class_member(models.Model):
#     class_id = models.ForeignKey(student_class,on_delete = models.CASCADE,blank=True,null=True)
#     student = models.ForeignKey(User,on_delete = models.CASCADE,blank=True,null=True)
#
#     def __str__(self):
#         return str(self.id)


class attendence_schedule(models.Model):
    sclass = models.ForeignKey(sub_class,on_delete=models.CASCADE)
    subject = models.ForeignKey(faculty_handled_class,on_delete=models.CASCADE)
    date = models.DateField()
    status = models.BooleanField(default = False)

    def __str__(self):
        return str(self.subject)

class attendence(models.Model):
    subject = models.ForeignKey(attendence_schedule,on_delete=models.CASCADE)
    student = models.ForeignKey(User,on_delete=models.CASCADE)
    status = models.BooleanField(default=True)

    def __str__(self):
        return str(self.student)+" "+str(self.subject.subject)

class attendence_count(models.Model):
    total_class = models.IntegerField(default=0)
    attended_class = models.IntegerField(default=0)
    student = models.ForeignKey(User,on_delete=models.CASCADE)
    sclass = models.ForeignKey(sub_class,on_delete=models.CASCADE)
    subject = models.ForeignKey(faculty_handled_class,on_delete=models.CASCADE)

    def __str__(self):
        return str(self.student)+" "+str(self.subject)

class test_type(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50,blank=True,null=True)
    code = models.CharField(max_length=10,blank=True,null=True)
    max_marks = models.IntegerField(default=10,blank=True,null=True)
    pass_marks = models.IntegerField(default=4,blank=True,null=True)

    def __str__(self):
        return str(self.id)+" "+str(self.code)

class test(models.Model):
    subject_handler = models.ForeignKey(faculty_handled_class,on_delete=models.CASCADE)
    test_type = models.ForeignKey(test_type,on_delete=models.CASCADE)
    class_id = models.ForeignKey(sub_class,on_delete=models.CASCADE)
    subject_id = models.ForeignKey(class_subject,on_delete=models.CASCADE)

    def __str__(self):
        return str(self.subject_handler.faculty_id) +" "+str(self.test_type.code)


class marks(models.Model):
    test_id = models.ForeignKey(test,on_delete=models.CASCADE)
    student = models.ForeignKey(User,on_delete=models.CASCADE)
    marks_obtained = models.IntegerField(default=0)

    def __str__(self):
        return str(self.student.first_name)+" "+str(self.test_id.test_type.code)













#
