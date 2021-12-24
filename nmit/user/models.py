from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class user_status(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class role(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20)

    def __str__(self):
        return str(self.id)+" "+self.name

class user_profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    role_id = models.ForeignKey(role,on_delete = models.CASCADE,blank=True,null=True)
    user_status = models.ForeignKey(user_status,on_delete = models.CASCADE,blank=True,null=True)

    def __str__(self):
        return str(self.user)
