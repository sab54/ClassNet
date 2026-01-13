from django.test import TestCase
from django import forms
from django.contrib.auth import get_user_model
from communication.models import StatusUpdate
from communication.forms import StatusUpdateForm

CustomUser = get_user_model()

class StatusUpdateFormTest(TestCase):

    def setUp(self):
        """
        Set up the necessary data for testing.
        """
        # Create a student user
        self.user = get_user_model().objects.create_user(
            username='testuser',
            first_name='Student',
            last_name='User',
            email='student_user@example.com',
            password='password',
            user_type='student',
            is_staff=False,
        )

    def test_form_valid_data(self):
        """
        Test that the form is valid when provided with valid data.
        """
        form_data = {'content': 'This is a new status update.'}
        form = StatusUpdateForm(data=form_data)

        # The form should be valid
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['content'], 'This is a new status update.')

    def test_form_invalid_data_missing_content(self):
        """
        Test that the form is invalid when content is missing.
        """
        form_data = {'content': ''}
        form = StatusUpdateForm(data=form_data)

        # The form should be invalid because the content is empty
        self.assertFalse(form.is_valid())
        self.assertIn('content', form.errors)

    def test_form_saves_data_to_model(self):
        """
        Test that the form correctly saves data to the StatusUpdate model.
        """
        form_data = {'content': 'This is a status update.'}
        form = StatusUpdateForm(data=form_data)

        # Check if the form is valid
        self.assertTrue(form.is_valid())

        # Save the form data to the model
        status_update = form.save(commit=False)
        status_update.user = self.user  # Set the user before saving (assuming it's required)
        status_update.save()

        # Verify the data was saved correctly in the model
        saved_status_update = StatusUpdate.objects.get(id=status_update.id)
        self.assertEqual(saved_status_update.content, 'This is a status update.')
        self.assertEqual(saved_status_update.user, self.user)

    def test_widget_attributes(self):
        """
        Test that the content field widget has the correct attributes.
        """
        form = StatusUpdateForm()

        # Get the widget for the 'content' field
        content_widget = form.fields['content'].widget

        # Check if the widget is a Textarea
        self.assertIsInstance(content_widget, forms.Textarea)

        # Check if the placeholder is correct
        self.assertEqual(content_widget.attrs['placeholder'], 'What’s on your mind?')

        # Check if the number of rows is set to 3
        self.assertEqual(content_widget.attrs['rows'], 3)

    def test_form_initial_data(self):
        """
        Test that the form initializes with the correct initial data.
        """
        form = StatusUpdateForm()

        # Check if the initial value for content is None (since no initial data is passed)
        self.assertIsNone(form.initial.get('content'))

