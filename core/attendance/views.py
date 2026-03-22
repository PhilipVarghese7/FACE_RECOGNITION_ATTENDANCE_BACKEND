from django.shortcuts import render
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from datetime import date
import numpy as np

from students.models import Student
from .models import StudentAttendance, GuestAttendance
from .serializers import StudentAttendanceSerializer, GuestAttendanceSerializer
from .utils import img_to_rgb_array, largest_face, cosine_similarity, app

THRESHOLD = 0.52  # similarity threshold


# -----------------------------
# HTML Page Views
# -----------------------------
def home_page(request):
    """Home page"""
    return render(request, "index.html")


def attendance_page(request):
    """Live attendance page with camera"""
    return render(request, "attendance.html")

def today_attendance_page(request):
    return render(request, "today.html")

# API for today’s status
class TodayAttendanceView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        today = date.today()
        students = Student.objects.filter(user=request.user)   # only this user’s students
        attendance_records = StudentAttendance.objects.filter(
            marked_at__date=today,
            user=request.user                                  # filter by user too
        )

        attended_ids = set(a.student_id for a in attendance_records)
        response = []

        for student in students:
            record = next((a for a in attendance_records if a.student_id == student.id), None)
            response.append({
                "id": student.id,
                "roll_no": student.roll_no,
                "name": student.name,
                "status": "Present" if student.id in attended_ids else "Absent",
                "marked_at": record.marked_at if record else None,
                "photo": student.photo.url if student.photo else None,
            })

        return Response(response)

# -----------------------------
# API View to Mark Attendance
# -----------------------------
class MarkAttendanceView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        uploaded_file = request.FILES.get("image")
        if not uploaded_file:
            return Response({"error": "No image uploaded"}, status=400)

        try:
            # Convert file to RGB array
            img = img_to_rgb_array(uploaded_file)

            # Detect faces using InsightFace
            faces = app.get(img)
            f = largest_face(faces)

            if not f:
                # No face → mark as guest
                guest = GuestAttendance.objects.create(user=request.user, image=uploaded_file)
                serializer = GuestAttendanceSerializer(guest)
                return Response({"message": "Guest recorded", "guest": serializer.data}, status=200)

            emb = f.embedding
            best_match, highest_sim = None, -1

            # Compare with all students of this user
            for student in Student.objects.filter(user=request.user):
                if student.embedding:
                    stored_emb = np.array(student.embedding, dtype=np.float32)
                    sim = cosine_similarity(stored_emb, emb)
                    if sim > highest_sim:
                        highest_sim, best_match = sim, student

            # Recognized student
            if highest_sim >= THRESHOLD and best_match:
                today = timezone.localdate()
                already_marked = StudentAttendance.objects.filter(
                    student=best_match, marked_at__date=today, user=request.user
                ).exists()

                if already_marked:
                    return Response({"message": f"Attendance already marked for {best_match.name}"}, status=200)

                attendance = StudentAttendance.objects.create(
                    student=best_match, photo=uploaded_file, user=request.user
                )
                serializer = StudentAttendanceSerializer(attendance)
                return Response({"message": f"Attendance marked for {best_match.name}", "data": serializer.data}, status=200)

            else:
                # Face detected but no match → guest
                guest = GuestAttendance.objects.create(user=request.user, image=uploaded_file)
                serializer = GuestAttendanceSerializer(guest)
                return Response({"message": "Guest recorded", "guest": serializer.data}, status=200)

        except Exception as e:
            return Response({"status": "error", "message": str(e)}, status=500)


# -----------------------------
# List Views for Attendance Logs (per-user)
# -----------------------------
class StudentAttendanceList(generics.ListAPIView):
    serializer_class = StudentAttendanceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return StudentAttendance.objects.filter(user=self.request.user).order_by("-marked_at")


class GuestAttendanceList(generics.ListAPIView):
    serializer_class = GuestAttendanceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return GuestAttendance.objects.filter(user=self.request.user).order_by("-marked_at")
