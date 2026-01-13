from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CourseMaterial, StudentEnrollment, StudentNotification, TeacherNotification

@receiver(post_save, sender=StudentEnrollment)
def notify_teacher_on_enrollment(sender, instance, created, **kwargs):
    """
    Signal handler triggered when a new student enrollment is created.

    This function is connected to the `post_save` signal of the `StudentEnrollment` model.
    It fires whenever a new enrollment is created, and if the enrollment is new (created=True),
    a notification is generated for the teacher of the course that the student enrolled in.

    Arguments:
        sender: The model class that triggered the signal (`StudentEnrollment`).
        instance: The instance of the `StudentEnrollment` that was saved.
        created: A boolean indicating whether a new record was created (True) or an existing record was updated (False).
        kwargs: Additional keyword arguments passed by the signal (not used in this case).

    If the enrollment is newly created (`created=True`), the following actions occur:
        1. Fetch the course associated with the enrollment.
        2. Get the teacher of the course.
        3. Get the student who enrolled.
        4. Create a notification message that informs the teacher that a student has enrolled in their course.
        5. Create and save a `TeacherNotification` object with the message and the teacher as the recipient.

    This ensures that every time a student enrolls in a course, the teacher is notified about the new enrollment.

    Example:
        When a student named 'JohnDoe' enrolls in a course called 'Math 101', the teacher will receive a notification:
        "JohnDoe has enrolled in your course: Math 101."
    """
    if created:
        # Create a notification for the teacher
        course = instance.course
        teacher = course.teacher
        student = instance.student
        message = f"{student.username} has enrolled in your course: {course.name}."        
        # Create the notification
        TeacherNotification.objects.create(teacher=teacher, message=message)

@receiver(post_save, sender=CourseMaterial)
def notify_student_on_change_of_material(sender, instance, created, **kwargs):
    """
    Signal handler triggered when a course material is created or updated.

    This function is connected to the `post_save` signal of the `CourseMaterial` model.
    It fires whenever a new material is created or an existing material is updated. 
    When a material is created or updated, it sends a notification to all enrolled students
    in the corresponding course, informing them about the change in course materials.

    Arguments:
        sender: The model class that triggered the signal (`CourseMaterial`).
        instance: The instance of the `CourseMaterial` that was saved.
        created: A boolean indicating whether a new record was created (True) or an existing record was updated (False).
        kwargs: Additional keyword arguments passed by the signal (not used in this case).

    If a new material is created (`created=True`) or an existing material is updated, 
    the following actions occur:
        1. Get the course associated with the material.
        2. Retrieve all the students enrolled in the course.
        3. Create a notification message for each student about the new or updated material.
        4. Create and save a `StudentNotification` object for each enrolled student.

    This ensures that every time a new course material is added or updated, all enrolled students are notified.
    """
    if created:
        # Create a notification for the teacher
        course = instance.course
        teacher = instance.course.teacher
        description = instance.description
        message = f"{teacher.username} has added new material {description} in your course: {course.name}."
        # Create the notification
        StudentNotification.objects.create(message=message)
 