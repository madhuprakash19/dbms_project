from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class user_status(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20)

    def __str__(self):
        return str(self.id)+" "+self.name


class role(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20)

    def __str__(self):
        return str(self.id)+" "+self.name


class user_profile(models.Model):
    id = models.IntegerField(primary_key=True)
    email = models.EmailField(max_length=50)
    user_name = models.IntegerField()
    password = models.CharField(max_length=10)
    role_id = models.ForeignKey(User,related_name='role_id',on_delete = models.CASCADE,blank=True,null=True)
    user_status = models.ForeignKey(User,related_name='user_status',on_delete = models.CASCADE,blank=True,null=True)

    def __str__(self):
        return str(self.id)


#class user_model(models.Model):
