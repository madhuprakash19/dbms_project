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

# test comment
