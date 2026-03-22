from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="students",null=True, blank=True
    )  # link each student to its owner
    name = models.CharField(max_length=100)
    roll_no = models.CharField(max_length=50)
    photo = models.ImageField(upload_to="student_photos/")
    embedding = models.JSONField()  # store 512d embedding as list of floats

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("user", "roll_no")  # same roll_no can exist for different users

    def __str__(self):
        return f"{self.roll_no} - {self.name}"
