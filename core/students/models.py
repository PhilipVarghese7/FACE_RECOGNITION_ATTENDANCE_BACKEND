from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=100)
    roll_no = models.CharField(max_length=50, unique=True)
    photo = models.ImageField(upload_to='student_photos/')
    embedding = models.JSONField()  # store 512d embedding as list of floats

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.roll_no} - {self.name}"
