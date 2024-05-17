# from django.db import models
# from django.db import models
from djongo import models
from django.contrib.auth.models import User
# Create your models here.
import numpy as np
import json


# Create your models here.
class Interest(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=100)

    def __str__(self):
        return self.name

class FastTextVector(models.Model):
    id=models.AutoField(primary_key=True)
    title=models.CharField(max_length=255,blank=True)
    text = models.CharField(max_length=255)
    # vector = models.BinaryField()
    id_number=models.CharField(max_length=500,blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    vector = models.JSONField()
    sc_vector = models.JSONField()   # JSON formatında saklanacak

    def save_numpy_data(self, data):
        # NumPy dizisini JSON formatına dönüştürerek kaydedin
        self.vector = json.dumps(data.tolist())
    
    def get_numpy_data(self):
        # JSON formatındaki veriyi NumPy dizisine geri dönüştürün
        return np.array(json.loads(self.vector))
    

class Reader(models.Model):
    id=models.AutoField(primary_key=True)
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    interests=models.ManyToManyField(Interest,blank=True)
    article_list=models.ManyToManyField(FastTextVector,blank=True)
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
