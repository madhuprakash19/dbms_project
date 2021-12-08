from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class hostel(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20)
    type = models.CharField(max_length=10,default='BOYS')

    def __str__(self):
        return str(self.id)+" "+self.name


class department(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=10)
    HOD = models.ForeignKey(User,related_name='HOD',on_delete = models.CASCADE,blank=True,null=True)

    def __str__(self):
        return str(self.id)+" "+self.name

class designation(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=30)

    def __str__(self):
        return str(self.id)+" "+self.name

class faculty(models.Model):
    id = models.IntegerField(primary_key=True)
    user_id = models.ForeignKey(User,related_name='user_id',on_delete = models.CASCADE,blank=True,null=True)
    name = models.CharField(max_length=50)
    dept_id = models.ForeignKey(User,related_name='dept_id',on_delete = models.CASCADE,blank=True,null=True)
    email = models.EmailField(max_length=50)
    phone_number = models.IntegerField()
    dob = models.DateField(max_length=10)
    gender = models.CharField(max_length=20)
    designation_id = models.ForeignKey(User,related_name='designation_id',on_delete = models.CASCADE,blank=True,null=True)
    year_of_joining = models.IntegerField()
    address =  models.CharField(max_length=50)
    salary = models.IntegerField()


    def __str__(self):
        return str(self.id)+" "+self.related_name


class student_personal_details(models.Model):
    adm_no = models.IntegerField(primary_key=True)#this is both pk and fk donno how to merge them so mentioned only as pk
    dob = models.DateField(max_length=10)
    gender = models.CharField(max_length=20)
    father_name =  models.CharField(max_length=50)
    mother_name = models.CharField(max_length=50)
    guardian_name = models.CharField(max_length=50)
    student_phone_number = models.IntegerField()
    student_phone_number = models.IntegerField()
    student_mail = models.EmailField(max_length=50)
    parent_mail = models.EmailField(max_length=50)
    address =  models.CharField(max_length=50)


    def __str__(self):
        return str(self.adm_no)


class student_details(models.Model):
    adm_no = models.IntegerField(primary_key=True)
    usn = models.CharField(max_length=15)
    user_id = models.ForeignKey(User,related_name='users_id',on_delete = models.CASCADE,blank=True,null=True)
    current_year = models.IntegerField()
    year_of_joining = models.IntegerField()
    year_of_passout = models.IntegerField()
    dept_id = models.ForeignKey(User,related_name='dep_id',on_delete = models.CASCADE,blank=True,null=True)

    def __str__(self):
        return str(self.usn)


class student_hostel(models.Model):
    student_adm_no = models.IntegerField(primary_key=True)#pk and fk issue
    hostel_id = models.ForeignKey(User,related_name='hostel_id',on_delete = models.CASCADE,blank=True,null=True)
    room_no = models.IntegerField()


    def __str__(self):
        return str(self.student_adm_no)
