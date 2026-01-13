from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from communication.models import StatusUpdate

class StatusUpdateViewTestCase(TestCase):

    def setUp(self):
        # Create a student user
        self.student_user = get_user_model().objects.create_user(
            username='student_user',
            first_name='Student',
            last_name='User',
            email='student_user@example.com',
            password='password123',
            user_type='student',
            is_staff=False,
        )

        # Create a non-student user (e.g., a teacher)
        self.teacher_user = get_user_model().objects.create_user(
            username='teacher_user',
            first_name='Teacher',
            last_name='User',
            email='teacher_user@example.com',
            password='password123',
            user_type='teacher',
            is_staff=True,  # Ensure the user is a staff
        )

    def test_add_status_update_authenticated_student(self):
        # Log in as a student user
        self.client.login(username='student_user', password='password123')

        # Submit a status update
        response = self.client.post(reverse('add_status_update'), {
            'content': 'Test status update'
        })

        # Ensure the status update was posted successfully and the user is redirected back
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('add_status_update'))

        # Verify the status update is stored in the database
        status_update = StatusUpdate.objects.get(user=self.student_user)
        self.assertEqual(status_update.content, 'Test status update')

    def test_add_status_update_non_student_user(self):
        # Log in as a non-student user (e.g., a teacher)
        self.client.login(username='teacher_user', password='password123')

        # Try to post a status update
        response = self.client.post(reverse('add_status_update'), {
            'content': 'Test status update from a teacher'
        })

        # Ensure that the teacher cannot post a status update and is redirected with an error message
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))  # Redirect to home or another page
        # You can also check for the error message if it's set in your view
        # self.assertContains(response, "You must be a student to post a status update.")

    def test_view_status_update_list_authenticated_student(self):
        # Log in as a student user
        self.client.login(username='student_user', password='password123')

        # Post multiple status updates
        self.client.post(reverse('add_status_update'), {'content': 'Status 1'})
        self.client.post(reverse('add_status_update'), {'content': 'Status 2'})
        self.client.post(reverse('add_status_update'), {'content': 'Status 3'})

        # Access the status updates page
        response = self.client.get(reverse('add_status_update'))

        # Check if the status updates are displayed
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Status 1')
        self.assertContains(response, 'Status 2')
        self.assertContains(response, 'Status 3')

    def test_add_status_update_form_display_for_authenticated_student(self):
        # Log in as a student user
        self.client.login(username='student_user', password='password123')

        # Access the page to add a status update
        response = self.client.get(reverse('add_status_update'))

        # Check that the form is displayed
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<form')  # Ensure the form is present
        self.assertContains(response, 'name="content"')  # Ensure the content field is there

    def test_pagination_of_status_updates(self):
        # Log in as a student user
        self.client.login(username='student_user', password='password123')

        # Post 15 status updates
        for i in range(15):
            self.client.post(reverse('add_status_update'), {'content': f'Status {i+1}'})

        # Access the status updates page
        response = self.client.get(reverse('add_status_update') + '?page_status=2')

        # Ensure the second page is displayed
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Status 10')
        self.assertContains(response, 'Status 6')
        self.assertNotContains(response, 'Status 2')

    def test_status_update_ordering(self):
        # Log in as a student user
        self.client.login(username='student_user', password='password123')

        # Post multiple status updates with timestamps
        status_1 = self.client.post(reverse('add_status_update'), {'content': 'First status'})
        status_2 = self.client.post(reverse('add_status_update'), {'content': 'Second status'})
        status_3 = self.client.post(reverse('add_status_update'), {'content': 'Third status'})

        # Retrieve status updates from the database and check ordering
        status_updates = StatusUpdate.objects.all()

        # Verify the latest status updates appear first
        self.assertEqual(status_updates[0].content, 'Third status')
        self.assertEqual(status_updates[1].content, 'Second status')
        self.assertEqual(status_updates[2].content, 'First status')
