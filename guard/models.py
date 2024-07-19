# from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import AbstractUser
class Parent(AbstractUser):
    # Add any additional fields you want for the Parent model
    pass

class Child(models.Model):
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE, related_name='children')
    name = models.CharField(max_length=100)
    dateofbirth=models.DateTimeField(null=True)

    def __str__(self):
        return self.name
class Csv_data(models.Model):
    child=models.ForeignKey(Child,on_delete=models.CASCADE,related_name='ChildCSVData')
    FILE_TYPE_CHOICES = [
        ('oximeter values graph', 'Oximeter Values Graph'),
        ('accelo meter graph', 'Accelo Meter Graph'),
        ('perspiration sensor', 'Perspiration Sensor'),
    ]
    file_type = models.CharField(max_length=1000, choices=FILE_TYPE_CHOICES,null=True)
    data_file = models.FileField(upload_to='child_data/',null=True)
    is_latest=models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.child.name}+{self.data_file.file}"
