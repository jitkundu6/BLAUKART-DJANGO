from django.shortcuts import render

from django.contrib import messages
from .models import Contact


def form_submit(request):
	####################### POST: ##########################
	FAILED = False
	if request.method == 'POST':
		try:
			name = request.POST['name']
			email = request.POST['email']
			subject = request.POST['subject']
			message = request.POST['message']
			phone = request.POST['phone']
			
			contact = Contact(
				name=name,
				email=email,
				subject=subject,
				message=message,
				phone=phone,
			)
			contact.save()
			
			print(f"Your details have been successfully submitted!")
			messages.success(request, f"Your details have been successfully submitted!")
		
		except Exception as err:
			print(f"ErrorType- {type(err)}")
			print(f"Error- {err}")
			messages.error(request, f"Error - Please check the details & Try again!")
			FAILED = True
	
	return render(request, 'contact.html', {})
