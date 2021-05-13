
from django.db.models.signals import post_save, pre_save, post_migrate, post_delete
from django.dispatch import receiver, Signal

from .models import CustomUser

from django.contrib import messages

from django.utils.timezone import timedelta
from time import sleep

#from django.core.signals import request_finished, request_started, got_request_exception

#mysignal = Signal(providing_args=['name'])   # creating custom signal


from django.core.mail import send_mail
HOST_EMAIL = 'subhajit.webkrone@gmail.com'


user_logged_in = Signal()
user_login_failed = Signal()
user_logged_out = Signal()


@receiver(post_save, sender=CustomUser)                  # sender argument is optional, by default it would applied for all Models
def sendemail_postsignal(sender, instance, **kwargs):

	if(instance.last_updated - instance.date_joined < timedelta(0,0.1)):
		print("instance.last_updated :" ,instance.last_updated)
		print("instance.date_joined :" ,instance.date_joined)
		sleep(2)

		print("--Sending Greeting Email...")
		try:
			subject = "Congrats! Account Detalis Saved"
			message = f"""
	Hello {instance.get_full_name()}, \n Your account detail is saved successfully!
			"""

			rcvr_email = instance.email # user email id
			from_email =  'HOST_EMAIL'
			send_mail(subject, message, from_email, [rcvr_email], fail_silently=False)
			# send_mail('hi','hello! Sk','jitkundu6@gmail.com',["jitkundu6@gmail.com"],fail_silently=False)
			print("--Email sent...")

		except :
			print("--Unable to sent Email!")
			#messages.error(request, f'Unable to sent Email!')

		





