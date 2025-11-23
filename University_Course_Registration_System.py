from datetime import datetime

# =========================
# Base Person Class
# =========================
class Person:
    def __init__(self, person_id, name, email, phone=None):
        self.person_id = person_id
        self.name = name
        self.email = email
        self.phone = phone
        self.role = None

    def display_info(self):
        print(f"ID: {self.person_id}, Name: {self.name}, Email: {self.email}, Phone: {self.phone}")

    def update_contact(self, email, phone):
        self.email = email
        self.phone = phone
        print(f"{self.name}'s contact updated.")


# =========================
# Student Class
# =========================
class Student(Person):
    GRADE_POINTS = {"A": 4, "B": 3, "C": 2, "D": 1, "E": 0}

    def __init__(self, student_id, name, email, phone=None):
        super().__init__(student_id, name, email, phone)
        self.role = "Student"
        self.courses = []
        self.grades = {}       # course_code -> grade
        self.attendance = {}   # course_code -> list of booleans
        self.last_login = datetime.now()

    def register_course(self, course):
        if course.code not in [c.code for c in self.courses]:
            self.courses.append(course)
            print(f"{self.name} registered for {course.title}")
        else:
            print(f"{self.name} already registered for {course.title}")

    def calculate_gpa(self):
        if not self.grades:
            return 0.0
        total_points = sum(self.GRADE_POINTS.get(g, 0) for g in self.grades.values())
        return round(total_points / len(self.grades), 2)

    def calculate_attendance(self):
        if not self.attendance:
            return 0.0
        total_attended = sum(sum(1 for r in records if r) for records in self.attendance.values())
        total_possible = sum(len(records) for records in self.attendance.values())
        return (total_attended / total_possible * 100) if total_possible else 0

    def performance_summary(self):
        gpa = self.calculate_gpa()
        attendance = self.calculate_attendance()
        print(f"{self.name} | GPA: {gpa} | Attendance: {attendance:.1f}%")
        if gpa >= 3.5 and attendance >= 90:
            print("Excellent performance!")
        elif gpa < 2.0 or attendance < 60:
            print("Warning: Poor performance")
        else:
            print("Satisfactory performance")
        return gpa


# =========================
# Course Class
# =========================
class Course:
    def __init__(self, code, title, credit_hours, lecturer=None):
        self.code = code
        self.title = title
        self.credit_hours = credit_hours
        self.lecturer = lecturer
        self.students = []

    def enroll_student(self, student):
        if student not in self.students:
            self.students.append(student)
            student.register_course(self)
            print(f"{student.name} added to {self.title}")

    def assign_grades(self, grade):
        for student in self.students:
            student.grades[self.code] = grade
            print(f"Assigned grade {grade} to {student.name} for {self.code}")

    def display_details(self):
        lecturer_name = self.lecturer.name if self.lecturer else "TBA"
        print(f"{self.code}: {self.title}, Credits: {self.credit_hours}, Lecturer: {lecturer_name}")
        print("Enrolled students:")
        for s in self.students:
            print(f"- {s.name}")


# =========================
# Lecturer Class
# =========================
class Lecturer(Person):
    def __init__(self, staff_id, name, email, department):
        super().__init__(staff_id, name, email)
        self.role = "Lecturer"
        self.department = department
        self.courses = []

    def assign_course(self, course):
        if course not in self.courses:
            self.courses.append(course)
            course.lecturer = self
            print(f"{self.name} assigned to {course.title}")

    def print_summary(self):
        print(f"Lecturer: {self.name} ({self.department})")
        for course in self.courses:
            print(f"Teaching: {course.title} ({len(course.students)} students)")


# =========================
# Registrar Class
# =========================
class Registrar:
    def __init__(self):
        self.students = []
        self.courses = []
        self.lecturers = []

    def add_student(self, student):
        self.students.append(student)
        print(f"Added student {student.name}")

    def add_course(self, course):
        self.courses.append(course)

    def add_lecturer(self, lecturer):
        self.lecturers.append(lecturer)


# =========================
# University Reporter
# =========================
class UniversityReporter:
    @staticmethod
    def full_report(registrar: Registrar):
        print("\n=== University Report ===\n")
        print("Courses:")
        for course in registrar.courses:
            course.display_details()
            print()
        print("Lecturers:")
        for lecturer in registrar.lecturers:
            lecturer.print_summary()
            print()
        print("Students:")
        for student in registrar.students:
            student.performance_summary()
            print()


# =========================
# Main Program
# =========================
def main():
    registrar = Registrar()

    # Create courses
    c1 = Course("CS101", "Intro to Programming", 3)
    c2 = Course("CS201", "Data Structures", 4)
    registrar.add_course(c1)
    registrar.add_course(c2)

    # Create lecturer
    l1 = Lecturer("L001", "Dr. Smith", "smith@uni.com", "CS")
    registrar.add_lecturer(l1)
    l1.assign_course(c1)

    # Create students
    s1 = Student("S001", "Alice", "alice@uni.com")
    s2 = Student("S002", "Bob", "bob@uni.com")
    registrar.add_student(s1)
    registrar.add_student(s2)

    # Enroll students
    c1.enroll_student(s1)
    c1.enroll_student(s2)

    # Assign grades
    c1.assign_grades("A")

    # Attendance records
    s1.attendance["CS101"] = [True, True, False, True]
    s2.attendance["CS101"] = [True, False, True, False]

    # Generate report
    UniversityReporter.full_report(registrar)


if __name__ == "__main__":
    main()
