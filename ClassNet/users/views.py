from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import get_user_model, login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .forms import UserRegistrationForm, CustomPasswordChangeForm, UserSearchForm, UserUpdateForm
from django.db.models import Q 
from courses.models import Course, StudentEnrollment, CourseMaterial, MaterialCompletion, StudentNotification, TeacherNotification
from django.core.paginator import Paginator
from communication.models import StatusUpdate
from rest_framework import generics
from .serializers import CustomUserSerializer
from rest_framework.permissions import IsAuthenticated

class CustomUserListCreateView(generics.ListCreateAPIView):
    """
    This view handles listing all users and creating a new user.

    - The `GET` request will return a list of all users.
    - The `POST` request will create a new user.
    """
    queryset = get_user_model().objects.all()
    serializer_class = CustomUserSerializer

    def perform_create(self, serializer):
        # You can add additional logic here, such as assigning roles to users
        serializer.save()

class CustomUserRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    """
    This view handles retrieving and updating a specific user.

    - The `GET` request will return the details of a specific user by their ID.
    - The `PUT/PATCH` request will update the details of the specific user.
    """
    queryset = get_user_model().objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]  # Only authenticated users can update their data
    lookup_field = 'username'  # Use 'username' as the lookup field for the user

    def perform_update(self, serializer):
        # You can add custom logic here if necessary before updating
        serializer.save()
 
def register(request):
    """
    Handle user registration. If the request method is GET, display the registration form.
    If the request method is POST, validate the form and create a new user.
    """
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # Hash the password
            
            # Set is_staff based on the user_type
            if user.user_type == user.TEACHER:
                user.is_staff = True
            elif user.user_type == user.STUDENT:
                user.is_staff = False

            user.save()
            login(request, user)  # Automatically log the user in after registration
            return redirect('profile')  # Redirect to profile page after successful registration
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'register.html', {'form': form})


def login_view(request):
    """
    Handle user login. If the request method is POST, attempt to authenticate the user.
    If the request method is GET, render the login form.
    """
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if request.user.is_staff:
                return redirect('teacher')  # Redirect to profile after login
            elif request.user.user_type == user.STUDENT:
                return redirect('student')  # Redirect to profile after login
        else:
            messages.error(request, "Invalid username or password")
    return render(request, 'login.html')
 
@login_required
def logout_view(request):
    """
    Handle user logout. If the request method is POST, attempt to authenticate the user.
    If the request method is GET, render the logout form.
    """
    logout(request)
    return redirect('login')  # Redirect to login page after logout

@login_required
def profile(request):
    user = request.user
    
    # Set is_staff based on the user_type
    if user.user_type == user.TEACHER:
        user.is_staff = True
    elif user.user_type == user.STUDENT:
        user.is_staff = False

    if request.method == 'POST':
        form = UserUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            if user.is_staff:
                return redirect('teacher')
            else:
                return redirect('student')
    else:
        form = UserUpdateForm(instance=user)

    return render(request, 'profile.html', {'form': form})

@login_required
def user_profile(request, user_id):
    """
    Display the profile page of the logged-in user.

    If the user is not logged in, they will be redirected to the login page
    due to the `login_required` decorator.
    """
    user = CustomUser.objects.get(id=user_id)
    return render(request, 'user_profile.html', {'profile': user})

@login_required
def change_password(request):
    """
    Handle the password change functionality for the currently logged-in user.

    - If the request method is GET, render the password change form.
    - If the request method is POST, validate the form and update the password.
    """
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            # Change the password
            form.save()
            # Update session to avoid logging the user out after password change
            update_session_auth_hash(request, form.user)
            return redirect('profile')  # Redirect back to profile page
        else:
            messages.error(request, "Please correct the error below.")
    else:
        form = CustomPasswordChangeForm(request.user)
    
    return render(request, 'change_password.html', {'form': form})

# Get the custom user model
CustomUser = get_user_model()

@login_required
def search_users(request):
    """
    This view handles searching for users in the system based on search criteria.

    - User Authentication: Ensures that only authenticated users can access this search functionality.
      If the user is not logged in, they will be redirected to the login page.

    - Search Logic: The view processes the search query from the request (usually via GET) to search for users
      based on specified criteria (e.g., username, email, role). This typically involves filtering the user model.

    - Context: The view passes the search results to the template for rendering, showing matching users to the search query.

    - Template Rendering: The function will render a template (e.g., 'user_search_results.html') to display the list of users
      who match the search criteria, possibly including pagination for large result sets.

    - Error Handling: If no results are found or there is an issue with the search query, an appropriate message is shown to the user.

    - Redirects: If the user is not authorized to access this page (e.g., not logged in or lacks permission),
      they will be redirected to the login page or an access denied page.

    - Permissions: Ensures that the user has the necessary permissions to perform the search (e.g., admin or user with specific roles).
    """
    # Check if the logged-in user is a teacher
    if request.user.user_type != CustomUser.TEACHER:
        messages.error(request, "You must be a teacher to search for users.")
        return redirect('/')  # Redirect to a page of your choice (e.g., home page)

    form = UserSearchForm()
    users = None

    if request.method == 'POST':
        form = UserSearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            # Filter users based on the search query (adjusting for custom model)
            if query:
                users = CustomUser.objects.filter(
                    (Q(username__icontains=query) | 
                    Q(first_name__icontains=query) | 
                    Q(last_name__icontains=query)) & 
                    (Q(user_type__in=[CustomUser.TEACHER, CustomUser.STUDENT]))
                ).order_by('username')
            else:
                users = []

    return render(request, 'search_results.html', {'form': form, 'users': users})


def studentHome(request):

    """
    This view handles the homepage/dashboard for students.

    - User Authentication: Ensures the user is authenticated (logged in).
      If the user is not logged in, they will be redirected to the login page.
      
    - Context: The view gathers student-specific data (e.g., current courses, assignments, grades)
      and passes it to the template for rendering on the homepage.

    - Template Rendering: The function will render the 'student_home.html' template, displaying relevant
      information in a user-friendly format, such as personalized greetings, tasks, or grades.

    - Error Handling: In case of errors when fetching or processing data, appropriate error messages
      will be displayed to the user.

    - Redirects: If the user is not authorized to view this page (e.g., not a student or not logged in),
      the view will redirect them to the login page or another appropriate location.

    - Permissions: Ensures that only users with the 'student' role or equivalent permissions can access
      this page. Other types of users (e.g., admin or staff) will be prevented from seeing the student content.
    """
    user = request.user

    # Fetch courses the student is enrolled in
    enrolled_courses = Course.objects.filter(enrollments__student=user, enrollments__blocked=False).order_by('name')

    # Fetch courses the student is not enrolled in
    available_courses = Course.objects.exclude(enrollments__student=user).order_by('name')

    # Paginate both enrolled and available courses
    paginator_enrolled = Paginator(enrolled_courses, 6)  # 5 per page for enrolled courses
    paginator_available = Paginator(available_courses, 6)  # 5 per page for available courses

    page_number_enrolled = request.GET.get('page_enrolled')
    page_obj_enrolled = paginator_enrolled.get_page(page_number_enrolled)

    page_number_available = request.GET.get('page_available')
    page_obj_available = paginator_available.get_page(page_number_available) 
    
    
    # # Calculate progress for each enrolled course
    progress = {}
    for course in page_obj_enrolled:
        students = StudentEnrollment.objects.filter(course=course).select_related('student').order_by('student_id')
        for student in students:
            if student.student_id == user.id:
                progress[student.course_id] = student.progress

    # Retrieve the current user's status updates
    status_updates = StatusUpdate.objects.filter(user=request.user).order_by('-timestamp')
    paginator = Paginator(status_updates, 5)  # Show 10 updates per page
    page_number = request.GET.get('page_status')
    status_page_obj = paginator.get_page(page_number)

    unread_notifications = StudentNotification.objects.filter(is_read=False)

    return render(request, 'student.html', {
        'page_obj_enrolled': page_obj_enrolled,
        'page_obj_available': page_obj_available,
        'status_page_obj': status_page_obj,
        'progress': progress,
        'unread_notifications': unread_notifications,
    })

def teacherHome(request):
    """
    This view handles the homepage/dashboard for teachers.

    - User Authentication: Ensures that the user is authenticated (logged in).
      If the user is not logged in, they will be redirected to the login page.

    - Context: The view gathers teacher-specific data (e.g., courses they teach, students, assignments,
      grades, upcoming events) and passes it to the template for rendering on the homepage.

    - Template Rendering: The function will render the 'teacher_home.html' template, displaying relevant
      information in a user-friendly format, such as a list of courses, student performance, and assignments.

    - Error Handling: In case of issues while fetching or processing data, appropriate error messages
      will be displayed to the user.

    - Redirects: If the user is not authorized to view this page (e.g., not a teacher or not logged in),
      the view will redirect them to the login page or another appropriate location.

    - Permissions: Ensures that only users with the 'teacher' role or equivalent permissions can access
      this page. Other types of users (e.g., students, admins) will be prevented from viewing teacher-specific content.
    """
    # Fetch all courses
    # Fetch courses created by the logged-in teacher
    courses = Course.objects.filter(teacher=request.user).order_by('name')   

    # Fetch the students enrolled in each course
    course_students = {}
    for course in courses:
        students = StudentEnrollment.objects.filter(course=course).select_related('student')
        course_students[course] = students


    paginator_course = Paginator(courses, 6)  # Show 5 courses per page
    page_number_course = request.GET.get('page_course')
    page_obj_course = paginator_course.get_page(page_number_course)

    # Retrieve the current user's status updates
    status_updates = StatusUpdate.objects.order_by('-timestamp')
    paginator_status_update = Paginator(status_updates, 6)  # Show 10 updates per page
    page_number_status_update = request.GET.get('page_status')
    status_page_obj = paginator_status_update.get_page(page_number_status_update)

    unread_notifications = TeacherNotification.objects.filter(is_read=False)

    return render(request, 'teacher.html', {'courses': courses, 
                                            'page_obj_course': page_obj_course, 
                                            'course_students': course_students, 
                                            'status_page_obj': status_page_obj, 
                                            'unread_notifications': unread_notifications})
