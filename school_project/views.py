from django.views.generic import ListView, CreateView, UpdateView, View, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, get_object_or_404, render
from .models import Class, Student, Teacher, Schedule, Grade
from .forms import StudentForm, TeacherForm, GradeForm, ScheduleForm, ClassForm, LoginForm, RecoverForm, SetNewPasswordForm, CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from .services import send_emails

@login_required
def school_info(request):
    return render(request, 'index.html')

class PasswordResetConfirmView(View):
    template_name = 'reset_password.html'

    def get_user(self, uidb64):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            return User.objects.get(pk=uid)
        except (User.DoesNotExist, ValueError, TypeError):
            return None

    def get(self, request, uidb64, token):
        user = self.get_user(uidb64)

        if user and default_token_generator.check_token(user, token):
            form = SetNewPasswordForm()
            return render(request, self.template_name, {'form': form})
        
        return redirect('password_reset')

    def post(self, request, uidb64, token):
        user = self.get_user(uidb64)

        if user and default_token_generator.check_token(user, token):
            form = SetNewPasswordForm(request.POST)
            if form.is_valid():
                user.set_password(form.cleaned_data['new_password1'])
                user.save()
                return redirect('login')
            return render(request, self.template_name, {'form': form})
        
        return redirect('password_reset')

class RecoverPassword(FormView):
    template_name = 'forget.html'
    form_class = RecoverForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        email = form.cleaned_data['email']
        try:
            user = User.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)

            reset_link = self.request.build_absolute_uri(
                reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
            )
            subject = "Відновлення пароля"
            body = f"Привіт, {user.username}!\n\nЩоб скинути пароль, перейдіть за цим посиланням:\n{reset_link}"
            send_emails.send_recover(subject, body, user.email)

            return super().form_valid(form)

        except User.DoesNotExist:
            return redirect('password_reset')

class RegisterView(CreateView):
    template_name = 'register.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')

class LoginView(FormView):
    template_name = 'login.html'
    form_class = LoginForm
    success_url = reverse_lazy('school_info')  

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(self.request, username=username, password=password)
        if user is not None:
            login(self.request, user)
            return super().form_valid(form)
        else:
            form.add_error(None, 'Невірний логін або пароль')
            return self.form_invalid(form)
        

class TeacherView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        if 'pk' in kwargs:
            teacher = get_object_or_404(Teacher, pk=kwargs['pk'])
            form = TeacherForm(instance=teacher)
            return render(request, 'teacher_form.html', {'form': form, 'teacher': teacher})
        else:
            teachers = Teacher.objects.all()
            return render(request, 'teachers_list.html', {'teachers': teachers})

    def post(self, request, *args, **kwargs):
        if 'pk' in kwargs:
            teacher = get_object_or_404(Teacher, pk=kwargs['pk'])
            if 'delete' in request.POST:
                teacher.delete()
                return redirect('teacher_list')
            form = TeacherForm(request.POST, instance=teacher)
            if form.is_valid():
                form.save()
                return redirect('teacher_list')
        else:
            form = TeacherForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('teacher_list')
        return render(request, 'teacher_form.html', {'form': form})


class StudentView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        if 'pk' in kwargs:
            student = get_object_or_404(Student, pk=kwargs['pk'])
            form = StudentForm(instance=student)
            return render(request, 'student_form.html', {'form': form, 'student': student})
        else:
            students = Student.objects.all()
            return render(request, 'students_list.html', {'students': students})

    def post(self, request, *args, **kwargs):
        print(2)
        if 'pk' in kwargs:
            student = get_object_or_404(Student, pk=kwargs['pk'])
            if 'delete' in request.POST:
                student.delete()
                return redirect('student_list')
            form = StudentForm(request.POST, instance=student)
            if form.is_valid():
                form.save()
                return redirect('student_list')
        else:
            form = StudentForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('student_list')
        return render(request, 'student_form.html', {'form': form})


class GradeView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        if 'pk' in kwargs:
            grade = get_object_or_404(Grade, pk=kwargs['pk'])
            form = GradeForm(instance=grade)
            return render(request, 'grade_form.html', {'form': form, 'grade': grade})
        else:
            grades = Grade.objects.all()
            return render(request, 'grades_list.html', {'grades': grades})

    def post(self, request, *args, **kwargs):
        if 'pk' in kwargs:
            grade = get_object_or_404(Grade, pk=kwargs['pk'])
            if 'delete' in request.POST:
                grade.delete()
                return redirect('grade_list')
            form = GradeForm(request.POST, instance=grade)
            if form.is_valid():
                form.save()
                return redirect('grade_list')
        else:
            form = GradeForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('grade_list')
        return render(request, 'grade_form.html', {'form': form})


class ScheduleView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        if 'pk' in kwargs:
            schedule = get_object_or_404(Schedule, pk=kwargs['pk'])
            form = ScheduleForm(instance=schedule)
            return render(request, 'schedule_form.html', {'form': form, 'schedule': schedule})
        else:
            schedules = Schedule.objects.all()
            return render(request, 'schedule_list.html', {'schedules': schedules})

    def post(self, request, *args, **kwargs):
        if 'pk' in kwargs:
            schedule = get_object_or_404(Schedule, pk=kwargs['pk'])
            if 'delete' in request.POST:
                schedule.delete()
                return redirect('schedule_list')
            form = ScheduleForm(request.POST, instance=schedule)
            if form.is_valid():
                form.save()
                return redirect('schedule_list')
        else:
            form = ScheduleForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('schedule_list')
        return render(request, 'schedule_form.html', {'form': form})


class ClassView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        if 'pk' in kwargs:
            class_obj = get_object_or_404(Class, pk=kwargs['pk'])
            form = ClassForm(instance=class_obj)
            return render(request, 'class_form.html', {'form': form, 'class': class_obj})
        else:
            classes = Class.objects.all()
            return render(request, 'class_list.html', {'classes': classes})

    def post(self, request, *args, **kwargs):
        if 'pk' in kwargs:
            class_obj = get_object_or_404(Class, pk=kwargs['pk'])
            print(request.POST)
            if 'delete' in request.POST:
                class_obj.delete()
                return redirect('class_list')
            form = ClassForm(request.POST, instance=class_obj)
            if form.is_valid():
                form.save()
                return redirect('class_list')
        else:
            form = ClassForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('class_list')
        return render(request, 'class_form.html', {'form': form})
