from django import forms
from .models import Student, Teacher, Subject, Grade, Schedule, Class
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'Email'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class SetNewPasswordForm(forms.Form):
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Новий пароль', 'class': 'form-control'}),
        label='Новий пароль',
        strip=False
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Підтвердження пароля', 'class': 'form-control'}),
        label='Підтвердження пароля',
        strip=False
    )

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get("new_password1")
        p2 = cleaned_data.get("new_password2")

        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("Паролі не співпадають!")
        return cleaned_data

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)

class RecoverForm(forms.Form):
    email = forms.CharField(widget=forms.EmailInput)

class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['name', 'email', 'phone_number', 'age']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Ім’я вчителя'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Електронна пошта'}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'Номер телефону'}),
            'age': forms.NumberInput(attrs={'placeholder': 'Вік'}),
        }

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'class_group', 'birthday', 'email', 'phone_number']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Ім’я студента'}),
            'class_group': forms.Select(attrs={'placeholder': 'Оберіть клас'}),
            'birthday': forms.DateInput(attrs={'type': 'date'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Електронна пошта'}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'Номер телефону'}),
        }

class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ['student', 'subject', 'grade']
        widgets = {
            'student': forms.Select(),
            'subject': forms.Select(),
            'grade': forms.NumberInput(attrs={'placeholder': 'Оцінка (1-12)'}),
        }

class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ['class_group', 'subject', 'teacher', 'day_of_week', 'time']
        widgets = {
            'class_group': forms.Select(),
            'subject': forms.Select(),
            'teacher': forms.Select(),
            'day_of_week': forms.Select(),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }

class ClassForm(forms.ModelForm):
    class Meta:
        model = Class
        fields = ['name']
        
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if Class.objects.filter(name=name).exists():
            raise forms.ValidationError("Клас з таким ім'ям вже існує.")
        return name