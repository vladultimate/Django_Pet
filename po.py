import django
import os

# Налаштування Django для роботи поза середовищем сервера
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'orm_test.settings')
django.setup()

from school_project.models import Student, Teacher, Class, Subject, Grade, Schedule

def add_student():
    name = input("Введіть ім'я студента: ")
    class_name = input("Введіть клас (наприклад, 10-А): ")
    class_group, created = Class.objects.get_or_create(name=class_name)
    birthday = input("Введіть дату народження (РРРР-ММ-ДД): ")
    email = input("Введіть email: ")
    phone = input("Введіть номер телефону: ")
    student = Student(name=name, class_group=class_group, birthday=birthday, email=email, phone_number=phone)
    student.save()
    print(f"✅ Студента '{name}' додано в клас {class_name}!")

def view_students():
    students = Student.objects.all()
    if not students:
        print("❌ Студентів ще немає.")
        return
    print("\n📚 Список студентів:")
    for student in students:
        print(f"{student.id}. {student.name} ({student.class_group.name}) - {student.email}")

def add_teacher():
    name = input("Введіть ім'я вчителя: ")
    email = input("Введіть email: ")
    phone = input("Введіть номер телефону: ")
    teacher = Teacher(name=name, email=email, phone_number=phone)
    teacher.save()
    print(f"✅ Вчителя '{name}' додано!")

def view_teachers():
    teachers = Teacher.objects.all()
    if not teachers:
        print("❌ Вчителів ще немає.")
        return
    print("\n🎓 Список вчителів:")
    for teacher in teachers:
        print(f"{teacher.id}. {teacher.name} - {teacher.email}")

def add_subject():
    """Додає новий предмет у базу"""
    subject_name = input("Введіть назву предмету: ")
    subject, created = Subject.objects.get_or_create(name=subject_name)
    if created:
        print(f"✅ Предмет '{subject_name}' додано!")
    else:
        print(f"⚠️ Предмет '{subject_name}' вже існує.")

def add_grade():
    student_name = input("Введіть ім'я студента: ")
    subject_name = input("Введіть предмет: ")
    grade_value = int(input("Введіть оцінку (0-12): "))
    try:
        student = Student.objects.get(name=student_name)
        subject = Subject.objects.get(name=subject_name)
        grade = Grade(student=student, subject=subject, grade=grade_value)
        grade.save()
        print(f"✅ Оцінку {grade_value} виставлено для {student_name} з предмету {subject_name}")
    except Student.DoesNotExist:
        print("❌ Студента з таким ім'ям немає.")
    except Subject.DoesNotExist:
        print("❌ Предмет не знайдено.")

def view_grades():
    student_name = input("Введіть ім'я студента: ")
    try:
        student = Student.objects.get(name=student_name)
        grades = Grade.objects.filter(student=student)
        if not grades:
            print("❌ У студента ще немає оцінок.")
            return
        print(f"\n📊 Оцінки для {student_name}:")
        for grade in grades:
            print(f"{grade.date} - {grade.subject.name}: {grade.grade}")
    except Student.DoesNotExist:
        print("❌ Студента з таким ім'ям немає.")

def delete_grade():
    student_name = input("Введіть ім'я студента: ")
    subject_name = input("Введіть предмет: ")
    try:
        student = Student.objects.get(name=student_name)
        subject = Subject.objects.get(name=subject_name)
        grade = Grade.objects.filter(student=student, subject=subject).last()
        if grade:
            grade.delete()
            print("🗑️ Оцінку видалено.")
        else:
            print("❌ Оцінки з цього предмету не знайдено.")
    except Student.DoesNotExist:
        print("❌ Студента з таким ім'ям немає.")
    except Subject.DoesNotExist:
        print("❌ Предмет не знайдено.")

def add_schedule():
    class_name = input("Введіть клас (наприклад, 10-А): ")
    subject_name = input("Введіть предмет: ")
    teacher_name = input("Введіть ім'я вчителя: ")
    day = input("Введіть день тижня: ")
    time = input("Введіть час уроку (HH:MM): ")
    try:
        class_group = Class.objects.get(name=class_name)
        subject = Subject.objects.get(name=subject_name)
        teacher = Teacher.objects.get(name=teacher_name)
        schedule = Schedule(class_group=class_group, subject=subject, teacher=teacher, day_of_week=day, time=time)
        schedule.save()
        print(f"✅ Додано розклад для {class_name} на {day} о {time}")
    except (Class.DoesNotExist, Subject.DoesNotExist, Teacher.DoesNotExist):
        print("❌ Клас, предмет або вчитель не знайдені.")

def view_schedule():
    class_name = input("Введіть клас (наприклад, 10-А): ")
    try:
        class_group = Class.objects.get(name=class_name)
        schedules = Schedule.objects.filter(class_group=class_group)
        if not schedules:
            print("❌ Розкладу для цього класу ще немає.")
            return
        print(f"\n📅 Розклад для {class_name}:")
        for schedule in schedules:
            print(f"{schedule.day_of_week}, {schedule.time} - {schedule.subject.name} ({schedule.teacher.name})")
    except Class.DoesNotExist:
        print("❌ Клас не знайдено.")

def main():
    while True:
        print("\n🏫 Меню школи:")
        print("1. Додати студента")
        print("2. Показати всіх студентів")
        print("3. Додати вчителя")
        print("4. Показати всіх вчителів")
        print("5. Виставити оцінку")
        print("6. Показати оцінки студента")
        print("7. Видалити оцінку")
        print("8. Додати розклад")
        print("9. Показати розклад класу")
        print("10. Вийти")
        print("11. Додати предмет")

        choice = input("Виберіть опцію: ")
        if choice == "1":
            add_student()
        elif choice == "2":
            view_students()
        elif choice == "3":
            add_teacher()
        elif choice == "4":
            view_teachers()
        elif choice == "5":
            add_grade()
        elif choice == "6":
            view_grades()
        elif choice == "7":
            delete_grade()
        elif choice == "8":
            add_schedule()
        elif choice == "9":
            view_schedule()
        elif choice == "11":
            add_subject()
        elif choice == "10":
            break
        else:
            print("❌ Невірний вибір, спробуйте ще раз.")

if __name__ == "__main__":
    main()