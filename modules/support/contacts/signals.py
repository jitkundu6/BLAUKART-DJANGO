
from django.db.models.signals import post_save, pre_save, post_migrate, post_delete
from django.dispatch import receiver, Signal

from .models import Contact

from django.core.mail import send_mail


from django.utils.timezone import timedelta
from time import sleep


HOST_EMAIL = 'subhajit.webkrone@gmail.com'


@receiver(post_save, sender=Contact)                  # sender argument is optional, by default it would applied for all Models
def contacts_postsignal(sender, instance, **kwargs):

		print("--Sending Email by contacts_sendemail_postsignal()...")
		
		try:
			print("--Sending Greeting Email to Contact Person...")
			subject = "Greeting from Blaustock!"
			message = f"""
	Hello {instance.name},\nThanks for contacting us,\n
	will Get back to you soon!

	Regards,
	Blaustock Team
			"""

			rcvr_email = instance.email # user email id
			from_email = HOST_EMAIL
			send_mail(subject, message, from_email, [rcvr_email], fail_silently=False)
			print("-- Greeting Email sent...")
			
			print("--Sending Notification Email to Host...")
			subject = "Blaustock - Contact Form Submitted"
			message = f"""
				Received New Message.\n
				Name: {instance.name}
				Email ID: {instance.email}
				Subject: {instance.subject}
				Message: {instance.message}
				Phone  Number: {instance.phone}

				Regards,
				Blaustock Auto-Email
						"""
			
			rcvr_email = HOST_EMAIL  # user email id
			from_email = HOST_EMAIL
			send_mail(subject, message, from_email, [rcvr_email], fail_silently=False)
			print("-- Notification Email sent...")
			
		except :
			print("--Unable to sent Email!")

		





