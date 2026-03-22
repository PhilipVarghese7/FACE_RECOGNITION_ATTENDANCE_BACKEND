from django.urls import path
from .views import (
    attendance_page,
    MarkAttendanceView,
    StudentAttendanceList,
    GuestAttendanceList,
    home_page,
    today_attendance_page,   # new HTML page
    TodayAttendanceView      # new API endpoint
)

urlpatterns = [
    path("live/", attendance_page, name="attendance_live"),
    path("", home_page, name="home"),

    # APIs
    path("mark/", MarkAttendanceView.as_view(), name="mark_attendance"),
    path("students/", StudentAttendanceList.as_view(), name="student_list"),
    path("guests/", GuestAttendanceList.as_view(), name="guest_list"),
    path("today-status/", TodayAttendanceView.as_view(), name="today_status"),  # NEW

    # HTML page for today’s attendance
    path("today/", today_attendance_page, name="attendance_today"),  # NEW
]
