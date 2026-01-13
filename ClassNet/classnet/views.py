
from django.shortcuts import render
from courses.models import Course
from django.core.paginator import Paginator

def home(request):
    """
    View function that handles displaying the homepage with a list of courses.
    - Fetches all courses from the database, ordered by the date they were created (newest first).
    - Paginates the courses, displaying 6 courses per page.
    - Retrieves the current page number from the request and calculates the corresponding set of courses.
    - Renders the 'home.html' template, passing the list of all courses and the paginated page object to the template for display.

    Args:
        request (HttpRequest): The HTTP request object containing user data and request parameters.

    Returns:
        HttpResponse: The rendered HTML page with the paginated list of courses.
    """

    # Fetch all courses
    courses = Course.objects.all().order_by('-created_at')
    paginator = Paginator(courses, 6)  # Show 6 courses per page
    # Get the current page number from the GET parameters in the request (e.g., ?page=2)
    page_number = request.GET.get('page')
    # Retrieve the page of courses corresponding to the page number requested
    page_obj = paginator.get_page(page_number)
    # Render the 'home.html' template, passing both all courses and the paginated page object to the template
    return render(request, 'home.html', {'courses': courses, 'page_obj': page_obj})

