from django.db import models

from django import forms


# Create your models here.

class Users(models.Model):
    deviceId = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.CharField(max_length=300)
    updated_on = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Files(models.Model):
    name = models.CharField(max_length=500)
    filepath = models.FileField(upload_to='files/',
                                null=True, verbose_name="")
    updated_on = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name + ": " + str(self.filepath)
