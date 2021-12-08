from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class subject(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=10)
    dept_id = models.ForeignKey(User,related_name='depart_id',on_delete = models.CASCADE,blank=True,null=True)
    description = models.CharField(max_length=50)


    def __str__(self):
        return str(self.name)+" "+self.id



class subject_student_enrollment(models.Model):
    id = models.IntegerField(primary_key=True)
    adm_no = models.ForeignKey(User,related_name='adm_no',on_delete = models.CASCADE,blank=True,null=True)
    subject_id = models.ForeignKey(User,related_name='subject_id',on_delete = models.CASCADE,blank=True,null=True)

    def __str__(self):
        return str(self.id)


class subject_handler(models.Model):
    id = models.IntegerField(primary_key=True)
    subject_id = models.ForeignKey(User,related_name='subject_id',on_delete = models.CASCADE,blank=True,null=True)
    faculty_id = models.ForeignKey(User,related_name='faculty_id',on_delete = models.CASCADE,blank=True,null=True)
    class_id = models.ForeignKey(User,related_name='clas_id',on_delete = models.CASCADE,blank=True,null=True)
    is_active = models.BooleanField()


    def __str__(self):
        return str(self.id)



class class(models.Model):
    id = models.IntegerField(primary_key=True)
    sem = models.CharField(max_length=10)
    section = models.CharField(max_length=10)
    dept_id = models.ForeignKey(User,related_name='depar_id',on_delete = models.CASCADE,blank=True,null=True)
    academic_year = models.IntegerField()
    students = models.IntegerField()
    is_active = models.BooleanField()

    def __str__(self):
        return str(self.sem)+" "+self.section



class class_member(models.Model):
    id = models.IntegerField(primary_key=True)
    class_id = models.ForeignKey(User,related_name='class_id',on_delete = models.CASCADE,blank=True,null=True)
    student = models.ForeignKey(User,related_name='student',on_delete = models.CASCADE,blank=True,null=True)

    def __str__(self):
        return str(self.id)
