from django.db import models
from django.conf import settings

class Course(models.Model):
    """
    Model representing a course in the system.

    A course is taught by a teacher and can have many students enrolled. It includes a name,
    description, teacher, and creation timestamp.

    Fields:
        name (CharField): The name of the course.
        description (TextField): A detailed description of the course.
        teacher (ForeignKey): A foreign key linking to the user who is the teacher for the course.
        created_at (DateTimeField): The timestamp when the course was created.

    Methods:
        __str__(): Returns the name of the course as a human-readable string.
    """

    name = models.CharField(max_length=255)
    description = models.TextField()
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="courses_taught")
    created_at = models.DateTimeField(auto_now_add=True)    
    
    def __str__(self):
        return self.name

class StudentEnrollment(models.Model):
    """
    Model representing the enrollment of a student in a course.

    This model tracks which student is enrolled in which course, their progress,
    and whether they have been blocked. It also tracks the timestamp when they enrolled.

    Fields:
        course (ForeignKey): The course the student is enrolled in.
        student (ForeignKey): The student who is enrolled in the course.
        progress (DecimalField): A field representing the student's progress in the course (percentage).
        blocked (BooleanField): Indicates whether the student's enrollment is blocked.
        enrolled_at (DateTimeField): The timestamp when the student enrolled in the course.

    Meta:
        unique_together (tuple): Ensures that each student can only enroll in the same course once.

    Methods:
        __str__(): Returns a string representation of the student and course enrollment.
    """
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="enrollments")
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="enrollments")
    progress = models.DecimalField(max_digits=5, decimal_places=2, default=0) 
    blocked = models.BooleanField(default=False)
    enrolled_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('course', 'student')

    def __str__(self):
        return f"{self.student.username} enrolled in {self.course.name}"


class CourseMaterial(models.Model):
    """
    Model representing a material associated with a course.

    This model holds the file associated with the course (e.g., lecture notes, readings),
    along with a description and the timestamp of when it was uploaded.

    Fields:
        course (ForeignKey): The course to which the material belongs.
        file (FileField): The file representing the course material.
        description (CharField): A short description of the course material.
        uploaded_at (DateTimeField): The timestamp when the material was uploaded.

    Methods:
        __str__(): Returns a string representation of the material for the associated course.
    """
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="materials")
    file = models.FileField(upload_to='course_materials/')
    description = models.CharField(max_length=255, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Material for {self.course.name}"


class MaterialCompletion(models.Model):
    """
    Model representing a student's completion of a specific course material.

    This model tracks when a student has completed a particular material from a course.

    Fields:
        student (ForeignKey): The student who completed the material.
        material (ForeignKey): The material that was completed by the student.
        completed_at (DateTimeField): The timestamp when the student completed the material.

    Meta:
        unique_together (tuple): Ensures that each student can only complete a material once.

    Methods:
        __str__(): Returns a string representation of the student and material completion.
    """
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="completed_materials")
    material = models.ForeignKey(CourseMaterial, on_delete=models.CASCADE, related_name="completed_by")
    completed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'material')

    def __str__(self):
        return f"{self.student.username} completed {self.material.description}"

class TeacherNotification(models.Model):
    """
    Model representing a notification for a teacher.

    This model stores notifications intended for a teacher, which include the message
    and whether the teacher has read it.

    Fields:
        teacher (ForeignKey): The teacher who will receive the notification.
        message (TextField): The content of the notification message.
        date_created (DateTimeField): The timestamp when the notification was created.
        is_read (BooleanField): A flag indicating whether the teacher has read the notification.

    Methods:
        __str__(): Returns a string representation of the teacher and the notification.
    """
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="TeacherNotification", limit_choices_to={'is_staff': True})
    message = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Notification for {self.teacher.username}"

class StudentNotification(models.Model):
    """
    Model representing a notification for a student.

    This model stores notifications intended for a student, which include the message
    and whether the student has read it.

    Fields:
        message (TextField): The content of the notification message.
        date_created (DateTimeField): The timestamp when the notification was created.
        is_read (BooleanField): A flag indicating whether the student has read the notification.

    Methods:
        __str__(): Returns a string representation of the notification.
    """
    # student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="StudentNotification", default=1)
    message = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Notification for {self.teacher.username}"