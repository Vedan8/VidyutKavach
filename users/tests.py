# users/tests.py
from django.core.mail import send_mail
from django.test import TestCase

class EmailTest(TestCase):
    def test_send_email(self):
        send_mail(
            'Test Subject',
            'Test message body',
            'your-email@gmail.com',  # From email address
            ['recipient-email@example.com'],  # To email address
            fail_silently=False,
        )
        self.assertTrue(True)
