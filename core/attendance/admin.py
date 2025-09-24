from django.contrib import admin
from .models import StudentAttendance, GuestAttendance

@admin.register(StudentAttendance)
class StudentAttendanceAdmin(admin.ModelAdmin):
    list_display = ("student", "marked_at")
    list_filter = ("marked_at",)
    search_fields = ("student__name", "student__roll_no")

@admin.register(GuestAttendance)
class GuestAttendanceAdmin(admin.ModelAdmin):
    list_display = ("id", "marked_at")
    list_filter = ("marked_at",)
