from django.shortcuts import render
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics

import numpy as np

from students.models import Student
from .models import StudentAttendance, GuestAttendance
from .serializers import StudentAttendanceSerializer, GuestAttendanceSerializer
from .utils import img_to_rgb_array, largest_face, cosine_similarity, app

THRESHOLD = 0.52  # similarity threshold


# -----------------------------
# HTML Page View
# -----------------------------
def attendance_page(request):
    return render(request, "attendance.html")


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
                guest = GuestAttendance.objects.create(image=uploaded_file)
                serializer = GuestAttendanceSerializer(guest)
                return Response({"message": "Guest recorded", "guest": serializer.data}, status=200)

            emb = f.embedding
            best_match, highest_sim = None, -1

            # Compare with all students
            for student in Student.objects.all():
                if student.embedding:
                    stored_emb = np.array(student.embedding, dtype=np.float32)
                    sim = cosine_similarity(stored_emb, emb)
                    if sim > highest_sim:
                        highest_sim, best_match = sim, student

            # Recognized student
            if highest_sim >= THRESHOLD:
                today = timezone.localdate()
                already_marked = StudentAttendance.objects.filter(
                    student=best_match, marked_at__date=today
                ).exists()

                if already_marked:
                    return Response({"message": f"Attendance already marked for {best_match.name}"}, status=200)

                attendance = StudentAttendance.objects.create(student=best_match, photo=uploaded_file)
                serializer = StudentAttendanceSerializer(attendance)
                return Response({"message": f"Attendance marked for {best_match.name}", "data": serializer.data}, status=200)

            else:
                # Face detected but no match → guest
                guest = GuestAttendance.objects.create(image=uploaded_file)
                serializer = GuestAttendanceSerializer(guest)
                return Response({"message": "Guest recorded", "guest": serializer.data}, status=200)

        except Exception as e:
            return Response({"status": "error", "message": str(e)}, status=500)


# -----------------------------
# List Views for Attendance Logs
# -----------------------------
class StudentAttendanceList(generics.ListAPIView):
    queryset = StudentAttendance.objects.all().order_by("-marked_at")
    serializer_class = StudentAttendanceSerializer
    permission_classes = [IsAuthenticated]


class GuestAttendanceList(generics.ListAPIView):
    queryset = GuestAttendance.objects.all().order_by("-marked_at")
    serializer_class = GuestAttendanceSerializer
    permission_classes = [IsAuthenticated]
