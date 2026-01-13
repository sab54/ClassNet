# views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import StatusUpdateForm
from .models import StatusUpdate
from django.core.paginator import Paginator

from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import StatusUpdateSerializer


from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import StatusUpdate
from .serializers import StatusUpdateSerializer

@api_view(['GET', 'POST'])
def status_update_list(request):
    """
    View to list all status updates or create a new one.

    - If the request is a GET request, it returns a list of all status updates in JSON format.
    - If the request is a POST request, it creates a new status update with the provided data.

    Methods:
        GET: Retrieve and return a list of status updates.
        POST: Create a new status update from the request data.
    """
    
    if request.method == 'GET':
        # Fetch all status updates from the database
        status_updates = StatusUpdate.objects.all()
        
        # Serialize the status updates into a format suitable for response (e.g., JSON)
        serializer = StatusUpdateSerializer(status_updates, many=True)
        
        # Return the serialized data as a response
        return Response(serializer.data)

    elif request.method == 'POST':
        # Deserialize the incoming data into a StatusUpdate object
        serializer = StatusUpdateSerializer(data=request.data)
        
        # Check if the data is valid
        if serializer.is_valid():
            # Save the new status update to the database
            serializer.save()
            
            # Return the serialized data with a 201 CREATED status code
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        # If the data is invalid, return the errors with a 400 BAD REQUEST status code
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def status_update_detail(request, pk):
    """
    View to retrieve, update or delete a specific status update.

    - If the request is a GET request, it retrieves and returns the details of the status update.
    - If the request is a PUT request, it updates the status update with the provided data.
    - If the request is a DELETE request, it deletes the status update.

    Arguments:
        pk (int): The primary key of the status update to be retrieved, updated, or deleted.
    """
    
    try:
        # Attempt to retrieve the status update by its primary key
        status_update = StatusUpdate.objects.get(pk=pk)
    except StatusUpdate.DoesNotExist:
        # If the status update is not found, return a 404 NOT FOUND response
        return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        # Serialize the status update and return the data
        serializer = StatusUpdateSerializer(status_update)
        return Response(serializer.data)

    elif request.method == 'PUT':
        # Deserialize the updated data for the status update
        serializer = StatusUpdateSerializer(status_update, data=request.data)
        
        # Check if the updated data is valid
        if serializer.is_valid():
            # Save the updated status update to the database
            serializer.save()
            
            # Return the updated data with a 200 OK status code
            return Response(serializer.data)
        
        # If the data is invalid, return the errors with a 400 BAD REQUEST status code
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        # Delete the status update from the database
        status_update.delete()
        
        # Return a 204 NO CONTENT status code indicating successful deletion
        return Response(status=status.HTTP_204_NO_CONTENT)


@login_required
def add_status_update(request):
    # Check if the logged-in user is a student
    if request.user.user_type != 'student':
        messages.error(request, "You must be a student to post a status update.")
        return redirect('home')  # Redirect to home or any other page
    
    # Handle the form submission
    if request.method == 'POST':
        form = StatusUpdateForm(request.POST)
        if form.is_valid():
            status_update = form.save(commit=False)
            status_update.user = request.user  # Set the current user as the owner of the status update
            status_update.save()
            return redirect('add_status_update')  # Redirect to home to show the latest status updates
    else:
        form = StatusUpdateForm()

    # Retrieve the current user's status updates
    status_updates = StatusUpdate.objects.filter(user=request.user).order_by('-timestamp')
    paginator = Paginator(status_updates, 5)  # Show 10 updates per page
    page_number = request.GET.get('page_status')
    status_page_obj = paginator.get_page(page_number)

    return render(request, 'status_update.html', {'form': form, 'status_page_obj': status_page_obj})