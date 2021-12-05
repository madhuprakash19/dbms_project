from django.db import models

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
