from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from feedback.models import CourseFeedback
from .models import Course, StudentEnrollment, CourseMaterial, MaterialCompletion, StudentNotification, TeacherNotification
from .forms import CourseForm, CourseMaterialForm
from django.core.mail import send_mail
from django.urls import reverse
from django.core.paginator import Paginator
from django.contrib import messages
from chat.models import Message

from rest_framework import generics
from .serializers import CourseSerializer, StudentEnrollmentSerializer, CourseMaterialSerializer, MaterialCompletionSerializer, TeacherNotificationSerializer, StudentNotificationSerializer


class CourseListCreateView(generics.ListCreateAPIView):
    """
    This view handles the creation of a new course. It allows the user (likely an admin or instructor)
    to enter the course name and description. Upon successful form submission, the course is created
    and the user is redirected to a confirmation or course list page.
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def perform_create(self, serializer):
        # You can add logic here to associate the course with the logged-in teacher if needed.
        serializer.save()


class StudentEnrollmentListCreateView(generics.ListCreateAPIView):
    """
    This view handles the student enrollment process. It allows a student to choose a course to enroll in.
    Once the student selects a course, an enrollment record is created or updated.
    """
    queryset = StudentEnrollment.objects.all()
    serializer_class = StudentEnrollmentSerializer

    def perform_create(self, serializer):
        # Optionally, you can associate the enrollment with the current student.
        serializer.save()


class CourseMaterialListCreateView(generics.ListCreateAPIView):
    """
    This view allows an instructor to upload course materials (e.g., PDFs, Word files, etc.)
    for a specific course. It includes fields for the file and an optional description.
    """
    queryset = CourseMaterial.objects.all()
    serializer_class = CourseMaterialSerializer

    def perform_create(self, serializer):
        serializer.save()


class MaterialCompletionListCreateView(generics.ListCreateAPIView):
    queryset = MaterialCompletion.objects.all()
    serializer_class = MaterialCompletionSerializer

    def perform_create(self, serializer):
        serializer.save()


class TeacherNotificationListCreateView(generics.ListCreateAPIView):
    queryset = TeacherNotification.objects.all()
    serializer_class = TeacherNotificationSerializer

    def perform_create(self, serializer):
        # Optionally, associate the notification with the teacher.
        serializer.save()


class StudentNotificationListCreateView(generics.ListCreateAPIView):
    queryset = StudentNotification.objects.all()
    serializer_class = StudentNotificationSerializer

    def perform_create(self, serializer):
        serializer.save()

@login_required
def create_course(request):
    if request.user.is_staff:
        if request.method == 'POST':
            form = CourseForm(request.POST)
            if form.is_valid():
                course = form.save(commit=False)
                course.teacher = request.user
                course.save()

                # Use the course name directly as the room name
                room_name = course.name.replace(' ', '_')  # Replace spaces with underscores for URL safety

                Message.objects.create(
                    room_name=room_name,
                    message = f"Welcome to the {room_name}!!!",
                    user=request.user
                )


                return redirect(reverse('view_course', kwargs={'course_id': course.id}))
        else:
            form = CourseForm()
        return render(request, 'create_course.html', {'form': form})
    else:
        return redirect('home')

@login_required
def view_course(request, course_id):
    course = Course.objects.get(id=course_id)

    # Check if the current user is the teacher
    if request.user == course.teacher:
        enrollments = StudentEnrollment.objects.filter(course=course).order_by('enrolled_at')
        materials = CourseMaterial.objects.filter(course=course).order_by('uploaded_at')

        # Paginate the enrollments (students)
        student_paginator = Paginator(enrollments, 5)  # Show 5 students per page
        student_page_number = request.GET.get('student_page')  # Get the current page for students
        student_page_obj = student_paginator.get_page(student_page_number)

        # Paginate the course materials
        material_paginator = Paginator(materials, 5)  # Show 5 materials per page
        material_page_number = request.GET.get('material_page')  # Get the current page for materials
        material_page_obj = material_paginator.get_page(material_page_number)

        feedbacks =  CourseFeedback.objects.filter(course=course) 

        return render(request, 'view_course.html', {
            'course': course,
            'student_page_obj': student_page_obj,  # Pass the student page object to the template
            'material_page_obj': material_page_obj,
            'feedbacks': feedbacks,  # Pass the material page object to the template
        })
    
    # Check if the current user is the student
    elif request.user.user_type == 'student':
        materials = CourseMaterial.objects.filter(course=course).order_by('uploaded_at')

        # Check which materials are completed by the student
        completed_materials = MaterialCompletion.objects.filter(student=request.user).order_by('completed_at')
        completed_material_ids = completed_materials.values_list('material_id', flat=True).order_by('completed_at')

        # Paginate the course materials
        material_paginator = Paginator(materials, 5)  # Show 5 materials per page
        material_page_number = request.GET.get('material_page')  # Get the current page for materials
        material_page_obj = material_paginator.get_page(material_page_number)

        return render(request, 'view_course.html', {
            'course': course,
            'material_page_obj': material_page_obj,  # Pass the material page object to the template
            'completed_material_ids': completed_material_ids,  # Pass the completed materials' IDs
        })

    else:
        return redirect('home')


@login_required
def available_courses(request):
    courses = Course.objects.all().order_by('-created_at')
    return render(request, 'available_courses.html', {'courses': courses})

@login_required
def enroll_in_course(request, course_id):
    course = Course.objects.get(id=course_id)
    if not StudentEnrollment.objects.filter(course=course, student=request.user).exists():
        StudentEnrollment.objects.create(course=course, student=request.user)      
        return redirect('student')
    return redirect('student')


@login_required
def mark_as_read_teacher_notifications(request, notification_id):
    notification = TeacherNotification.objects.get(id=notification_id)
    notification.is_read = True
    notification.save()
    return redirect('teacher')

@login_required
def mark_as_read_student_notifications (request, notification_id):
    notification = StudentNotification.objects.get(id=notification_id)
    notification.is_read = True
    notification.save()
    return redirect('student')


def unenroll_from_course(request, course_id):
    # Make sure the user is authenticated and is a student
    user = request.user
    if user.is_authenticated and user.user_type == 'student':
        try:
            # Get the course
            course = Course.objects.get(id=course_id)

            # Try to find the enrollment
            enrollment = StudentEnrollment.objects.get(course=course, student=user)

            # Unenroll the student
            enrollment.delete()

            # Redirect back to the student home page after successful unenrollment
            return redirect('student')
        
        except StudentEnrollment.DoesNotExist:
            # If no enrollment exists, you might want to handle that
            return redirect('student')  # or show a message that they were not enrolled
    else:
        return redirect('login')  # Redirect to login page if not authenticated


@login_required
def add_material(request, course_id):
    course = Course.objects.get(id=course_id)
    if request.user == course.teacher:
        if request.method == 'POST':
            form = CourseMaterialForm(request.POST, request.FILES)
            if form.is_valid():
                material = form.save(commit=False)
                material.course = course
                material.save()
                return redirect(reverse('view_course', kwargs={'course_id': course.id}))
        else:
            form = CourseMaterialForm()
        return render(request, 'add_material.html', {'form': form, 'course': course})
    else:
        return redirect('home')
    

@login_required
def delete_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    # Check if the current user is the teacher of the course
    if request.user == course.teacher:
        # Delete associated enrollments
        StudentEnrollment.objects.filter(course=course).delete()
        
        # Delete associated course materials
        CourseMaterial.objects.filter(course=course).delete()
        
        # Delete the course itself
        course.delete()
        
        # Notify the user
        return redirect('teacher')  # Redirect to the available courses list or home
    
    else:
        messages.error(request, "You do not have permission to delete this course.")
        return redirect('home')  # Redirect to home if the user is not the teacher

@login_required
def mark_material_as_completed(request, material_id):
    if request.method == 'POST':
        # Get the list of material IDs that the student marked as completed
        student = request.user

        material = CourseMaterial.objects.get(id=material_id)
        # Ensure the student is enrolled in the course before marking the material as completed
        if StudentEnrollment.objects.filter(course=material.course, student=student).exists():
            if  MaterialCompletion.objects.filter(student=student, material=material).exists():
                MaterialCompletion.objects.filter(student=student, material=material).delete()
            else:
                MaterialCompletion.objects.get_or_create(student=student, material=material)

         # Update the course progress (you can store this in a field or use it dynamically as needed)
        total_materials = CourseMaterial.objects.filter(course=material.course).count()
        completed_materials = MaterialCompletion.objects.filter(student=student, material__course=material.course).count()
        if total_materials > 0:
            progress_percentage = (completed_materials / total_materials) * 100
        else:
            progress_percentage = 0    
   
        students = StudentEnrollment.objects.filter(course=material.course, student=student).order_by('enrolled_at')
        for student in students:            
            student.progress=progress_percentage
            student.save()
    else:
        messages.error(request, "Invalid request.")
    return redirect(reverse('view_course', kwargs={'course_id': material.course.id}))


@login_required
def block_student(request, course_id, student_id):
    # Get the course and student objects
    course = Course.objects.get(id=course_id)
    student_enrollment = StudentEnrollment.objects.get(course=course, student_id=student_id)

    # Block the student from accessing the course (you can add a 'blocked' flag to the StudentEnrollment model)
    student_enrollment.blocked = True  # Assuming you added a 'blocked' field to StudentEnrollment
    student_enrollment.save()

    # Redirect back to the teacher home page
    return redirect(reverse('view_course', kwargs={'course_id': course.id}))

@login_required
def unblock_student(request, course_id, student_id):
    # Get the course and student objects
    course = Course.objects.get(id=course_id)
    student_enrollment = StudentEnrollment.objects.get(course=course, student_id=student_id)

    # Block the student from accessing the course (you can add a 'blocked' flag to the StudentEnrollment model)
    student_enrollment.blocked = False  # Assuming you added a 'blocked' field to StudentEnrollment
    student_enrollment.save()

    # Redirect back to the teacher home page
    return redirect(reverse('view_course', kwargs={'course_id': course.id}))

@login_required
def remove_student(request, course_id, student_id):
    # Get the course and student objects
    course = Course.objects.get(id=course_id)
    student_enrollment = StudentEnrollment.objects.get(course=course, student_id=student_id)

    # Remove the student from the course
    student_enrollment.delete()

    # Redirect back to the teacher home page
    return redirect(reverse('view_course', kwargs={'course_id': course.id}))

def home(request):
    return render(request, 'base.html')
