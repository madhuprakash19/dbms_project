from django.db import models
from info.models import department
from django.contrib.auth.models import User

class subject(models.Model):
    name = models.CharField(max_length=50,blank=True,null=True)
    code = models.CharField(max_length=10,blank=True,null=True)
    dept_id = models.ForeignKey(department,on_delete = models.CASCADE,blank=True,null=True)
    description = models.CharField(max_length=50,blank=True,null=True)


    def __str__(self):
        return str(self.name)+" "+self.id

class student_class(models.Model):
    sem = models.CharField(max_length=10,blank=True,null=True)
    section = models.CharField(max_length=10,blank=True,null=True)
    dept_id = models.ForeignKey(department,on_delete = models.CASCADE,blank=True,null=True)
    academic_year = models.IntegerField(blank=True,null=True)
    students = models.ManyToManyField(User,through='class_member')
    is_active = models.BooleanField(blank=True,null=True)

    def __str__(self):
        return str(self.sem)+" "+self.section

class subject_student_enrollment(models.Model):
    student = models.ForeignKey(User,related_name='adm_no',on_delete = models.CASCADE,blank=True,null=True)
    subject_id = models.ForeignKey(subject,on_delete = models.CASCADE,blank=True,null=True)

    def __str__(self):
        return str(self.id)

class subject_handler(models.Model):
    subject_id = models.ForeignKey(subject,on_delete = models.CASCADE,blank=True,null=True)
    faculty_id = models.ForeignKey(User,on_delete = models.CASCADE,blank=True,null=True)
    class_id = models.ForeignKey(student_class,related_name='clas_id',on_delete = models.CASCADE,blank=True,null=True)
    is_active = models.BooleanField()

    def __str__(self):
        return str(self.id)

class class_member(models.Model):
    class_id = models.ForeignKey(student_class,on_delete = models.CASCADE,blank=True,null=True)
    student = models.ForeignKey(User,on_delete = models.CASCADE,blank=True,null=True)

    def __str__(self):
        return str(self.id)
