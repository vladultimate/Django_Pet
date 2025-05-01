from django.urls import path
from .views import *

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('school/', school_info, name='school_info'),

    path('teachers/', TeacherView.as_view(), name='teacher_list'),
    path('teachers/add/', TeacherView.as_view(), name='teacher_add'),
    path('teachers/edit/<int:pk>/', TeacherView.as_view(), name='edit_teacher'),
    path('teachers/delete/<int:pk>/', TeacherView.as_view(), name='delete_teacher'),
    
    path('students/', StudentView.as_view(), name='student_list'),
    path('students/add/', StudentView.as_view(), name='student_add'),
    path('students/edit/<int:pk>/', StudentView.as_view(), name='edit_student'),
    path('students/delete/<int:pk>/', StudentView.as_view(), name='delete_student'),

    path('grades/', GradeView.as_view(), name='grade_list'),
    path('grades/add/', GradeView.as_view(), name='add_grade'),
    path('grades/edit/<int:pk>/', GradeView.as_view(), name='edit_grade'),
    path('grades/delete/<int:pk>/', GradeView.as_view(), name='delete_grade'),

    path('schedules/', ScheduleView.as_view(), name='schedule_list'),
    path('schedules/add/', ScheduleView.as_view(), name='add_schedule'),
    path('schedules/edit/<int:pk>/', ScheduleView.as_view(), name='edit_schedule'),
    path('schedules/delete/<int:pk>/', ScheduleView.as_view(), name='delete_schedule'),

    path('classes/', ClassView.as_view(), name='class_list'),
    path('classes/add/', ClassView.as_view(), name='add_class'),
    path('classes/edit/<int:pk>/', ClassView.as_view(), name='edit_class'),
    path('classes/delete/<int:pk>/', ClassView.as_view(), name='delete_class'),

    path('password/reset/', RecoverPassword.as_view(), name='password_reset'),
    path('password/reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]