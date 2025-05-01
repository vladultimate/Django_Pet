from django.db import models
from django.core.exceptions import ValidationError

class School(models.Model):
    name = models.CharField(max_length=255, unique=True)
    address = models.TextField(blank=True)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.name



class Teacher(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, default="")
    age = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(age__gte=21),
                name="teacher_age_gte_21"
            ),
            models.CheckConstraint(
                check=models.Q(email__regex=r'^[\w\.-]+@[\w\.-]+\.\w+$'),
                name='teacher_valid_email_format'
            ),
            models.CheckConstraint(
                check=models.Q(name__regex=r'^[A-Za-zА-Яа-яІіЇїЄєҐґ\'\- ]+$'),
                name='teacher_valid_name_format'
            )
        ]

class Subject(models.Model):
    name = models.CharField(max_length=100, unique=True)
    teachers = models.ManyToManyField(Teacher, related_name="subjects")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class Class(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class Student(models.Model):
    name = models.CharField(max_length=100)
    class_group = models.ForeignKey(Class, on_delete=models.SET_NULL, null=True, blank=True)
    birthday = models.DateField()
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, default="")

    def __str__(self):
        return self.name

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(email__regex=r'^[\w\.-]+@[\w\.-]+\.\w+$'),
                name='student_valid_email_format'
            ),
            models.CheckConstraint(
                check=models.Q(name__regex=r'^[A-Za-zА-Яа-яІіЇїЄєҐґ\'\- ]+$'),
                name='student_valid_name_format'
            )
        ]

class Schedule(models.Model):
    class_group = models.ForeignKey(Class, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    day_of_week = models.CharField(
        max_length=10,
        choices=[
            ('Monday', 'Понеділок'),
            ('Tuesday', 'Вівторок'),
            ('Wednesday', 'Середа'),
            ('Thursday', 'Четвер'),
            ('Friday', 'П’ятниця')
        ]
    )
    time = models.TimeField()

    def __str__(self):
        return f"{self.class_group.name} | {self.subject.name} | {self.day_of_week} {self.time}"

    class Meta:
        ordering = ['class_group', 'day_of_week', 'time']

    def clean(self):
        if not self.teacher.subjects.filter(id=self.subject.id).exists():
            raise ValidationError("Вчитель не може викладати цей предмет.")

class Grade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    grade = models.PositiveIntegerField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.name} | {self.subject.name} | {self.grade}"

    class Meta:
        ordering = ['-date']
        unique_together = ['student', 'subject', 'date']
