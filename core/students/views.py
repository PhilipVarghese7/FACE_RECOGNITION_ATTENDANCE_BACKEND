from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Student
from .serializers import StudentSerializer
from .face_utils import get_embedding
from django.shortcuts import render

def students_page(request):
    return render(request, "students.html")

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def students_list_create(request):
    if request.method == 'GET':
        # ✅ Only fetch students for this logged-in user
        students = Student.objects.filter(user=request.user)
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            photo_file = request.FILES.get('photo')
            if not photo_file:
                return Response({"error": "Photo is required"}, status=status.HTTP_400_BAD_REQUEST)

            # Generate embedding before saving
            embedding = get_embedding(photo_file)
            if embedding is None:
                return Response({"error": "No face detected"}, status=status.HTTP_400_BAD_REQUEST)

            # ✅ Save with the logged-in user
            student = serializer.save(user=request.user, embedding=embedding)
            return Response(StudentSerializer(student).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def student_detail(request, pk):
    try:
        # ✅ Only allow access to own students
        student = Student.objects.get(pk=pk, user=request.user)
    except Student.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = StudentSerializer(student)
        return Response(serializer.data)

    if request.method == 'PUT':
        serializer = StudentSerializer(student, data=request.data, partial=True)
        if serializer.is_valid():
            student = serializer.save()
            if 'photo' in request.FILES:
                embedding = get_embedding(student.photo)
                if embedding:
                    student.embedding = embedding
                    student.save()
            return Response(StudentSerializer(student).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        student.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
