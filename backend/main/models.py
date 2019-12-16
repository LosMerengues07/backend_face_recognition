from django.db import models

# Create your models here.


class User(models.Model):

    username = models.CharField(max_length=256,unique=True)
    password = models.CharField(max_length=256)
    c_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username

    class Meta:
        ordering = ["-c_time"]
        verbose_name = "User"
        verbose_name_plural = "Users"


"""
class Record(models.Model):
    name = models.CharField(max_length=256)
    time = models.CharField(max_length=64)
    content = models.CharField(max_length=3000, default='')
    record_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=256)
    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-record_id"]
        verbose_name = "Record"
        verbose_name_plural = "Records"
"""


class Img(models.Model):
    username = models.CharField(max_length=256,default='')
    raw_url = models.ImageField(upload_to='static/img/raw',default='None')
    cook1_url = models.CharField(max_length=2560,default='None')
    cook2_url = models.CharField(max_length=2560,default='None')
    c_time = models.DateTimeField(auto_now_add=True)
    img_id = models.AutoField(primary_key=True)

    class Meta:
        ordering = ["-c_time"]
        verbose_name = "Img"
        verbose_name_plural = "Imgs"
