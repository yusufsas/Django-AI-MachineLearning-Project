from django.db import models
from django.db import models
from django.contrib.auth.models import User
# Create your models here.


# Create your models here.
class Interest(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Reader(models.Model):
    id=models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    interests=models.ManyToManyField(Interest,blank=True)
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


