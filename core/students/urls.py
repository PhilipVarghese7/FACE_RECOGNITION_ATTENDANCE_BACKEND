from django.urls import path
from . import views

urlpatterns = [
    path("page/", views.students_page, name="students_page"),
    path('students/', views.students_list_create),
    path('students/<int:pk>/', views.student_detail),
]
