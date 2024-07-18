from django.contrib.auth.models import User
from django.db import models

class Parent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Child(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE, related_name='children')

    def __str__(self):
        return self.name
class Csv_data(models.Model):
    child=models.ForeignKey(Child,on_delete=models.CASCADE,related_name='ChildCSVData')
    FILE_TYPE_CHOICES = [
        ('oximeter values graph', 'Oximeter Values Graph'),
        ('ppG sensor graph', 'PPG Sensor Graph'),
        ('perspiration sensor', 'Perspiration Sensor'),
    ]
    file_type = models.CharField(max_length=1000, choices=FILE_TYPE_CHOICES,null=True)
    data_file = models.FileField(upload_to='child_data/',null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.child.name}+{self.data_file.file}"
