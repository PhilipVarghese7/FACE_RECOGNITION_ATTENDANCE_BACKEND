from django.db import models
from students.models import Student
from django.contrib.auth.models import User

class StudentAttendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="attendance")
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)  # Admin who marks attendance
    photo = models.ImageField(upload_to="student_attendance/", null=True, blank=True)
    marked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.name} - {self.marked_at}"
    
class GuestAttendance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)  # Admin who records guest
    image = models.ImageField(upload_to="guest_attendance/")
    marked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Guest - {self.marked_at}"
