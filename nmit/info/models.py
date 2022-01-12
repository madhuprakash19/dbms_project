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

#
# class faculty(models.Model):
#     user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
#     name = models.CharField(max_length=50,blank=True,null=True)
#     dept_id = models.ForeignKey(User,related_name='dept_id',on_delete = models.CASCADE,blank=True,null=True)
#     email = models.EmailField(max_length=50,blank=True,null=True)
#     phone_number = models.IntegerField(blank=True,null=True)
#     dob = models.DateField(max_length=10,blank=True,null=True)
#     gender = models.CharField(max_length=20,blank=True,null=True)
#     designation_id = models.ForeignKey(User,related_name='designation_id',on_delete = models.CASCADE,blank=True,null=True)
#     year_of_joining = models.IntegerField(blank=True,null=True)
#     address =  models.CharField(max_length=50,blank=True,null=True)
#     salary = models.IntegerField(blank=True,null=True)
#     new_dept = models.ForeignKey(department,on_delete = models.CASCADE,blank=True,null=True,default = 1)
#
#
#     def __str__(self):
#         return str(self.id)+" "+self.related_name


class teacher(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    name = models.CharField(max_length=50,blank=True,null=True)
    dept_id = models.ForeignKey(department,related_name='dept_id',on_delete = models.CASCADE,blank=True,null=True)
    email = models.EmailField(max_length=50,blank=True,null=True)
    phone_number = models.IntegerField(blank=True,null=True)
    dob = models.DateField(max_length=10,blank=True,null=True)
    gender = models.CharField(max_length=20,blank=True,null=True)
    designation_id = models.ForeignKey(designation,related_name='designation_id',on_delete = models.CASCADE,blank=True,null=True)
    year_of_joining = models.IntegerField(blank=True,null=True)
    address =  models.CharField(max_length=50,blank=True,null=True)
    salary = models.IntegerField(blank=True,null=True)


    def __str__(self):
        return str(self.id)+" "+self.related_name

class student_details(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    name = models.CharField(max_length=50,blank=True,null=True)
    adm_no = models.IntegerField(blank=True,null=True)
    usn = models.CharField(max_length=15,blank=True,null=True)
    current_year = models.IntegerField(blank=True,null=True)
    year_of_joining = models.IntegerField(blank=True,null=True)
    year_of_passout = models.IntegerField(blank=True,null=True)
    dept_id = models.ForeignKey(department,on_delete = models.CASCADE,blank=True,null=True)
    dob = models.DateField(blank=True,null=True)
    gender = models.CharField(max_length=20,blank=True,null=True)
    father_name =  models.CharField(max_length=50,blank=True,null=True)
    mother_name = models.CharField(max_length=50,blank=True,null=True)
    guardian_name = models.CharField(max_length=50,blank=True,null=True)
    student_phone_number = models.IntegerField(blank=True,null=True)
    parent_phone_number = models.IntegerField(blank=True,null=True)
    student_mail = models.EmailField(max_length=50,blank=True,null=True)
    parent_mail = models.EmailField(max_length=50,blank=True,null=True)
    address =  models.CharField(max_length=50,blank=True,null=True)

    def __str__(self):
        return str(self.usn)


class student_hostel(models.Model):
    student_adm_no = models.ForeignKey(User,on_delete = models.CASCADE,blank=True,null=True)
    hostel_id = models.ForeignKey(hostel,on_delete = models.CASCADE,blank=True,null=True)
    room_no = models.IntegerField(blank=True,null=True)


    def __str__(self):
        return str(self.student_adm_no)
