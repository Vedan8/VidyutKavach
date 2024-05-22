# myapp/adapters.py

from allauth.account.adapter import DefaultAccountAdapter
from django.urls import reverse

class CustomAccountAdapter(DefaultAccountAdapter):

    def send_confirmation_mail(self, request, emailconfirmation, signup):
        # Build the custom URL
        activate_url = reverse("confirm_email", args=[emailconfirmation.key])
        activate_url = request.build_absolute_uri(activate_url)
        
        # Custom email context
        ctx = {
            "user": emailconfirmation.email_address.user,
            "activate_url": activate_url,
            "key": emailconfirmation.key,
        }
        
        # Send the email using the custom context
        self.send_mail("account/email/email_confirmation", emailconfirmation.email_address.email, ctx)