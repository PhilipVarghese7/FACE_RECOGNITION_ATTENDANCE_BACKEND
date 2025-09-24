from django.urls import path
from .views import (
    attendance_page,
    MarkAttendanceView,
    StudentAttendanceList,
    GuestAttendanceList
)

urlpatterns = [
    # HTML page for live webcam attendance
    path("live/", attendance_page, name="attendance_live"),

    # API endpoint to mark attendance via POST (image upload)
    path("mark/", MarkAttendanceView.as_view(), name="mark_attendance"),

    # API endpoints to view attendance logs
    path("students/", StudentAttendanceList.as_view(), name="student_list"),
    path("guests/", GuestAttendanceList.as_view(), name="guest_list"),
]
