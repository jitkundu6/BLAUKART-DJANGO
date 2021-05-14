 
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
  
from . import forms as accounts_forms
from .forms import UserRegisterForm, UserRegisterLiteForm, LoginForm, UserUpdateForm#  PasswordChangeForm# AuthenticationForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm, SetPasswordForm
from django.contrib.auth import update_session_auth_hash

from django.http import HttpResponse
from django.shortcuts import render, redirect as _redirect


from django.contrib.auth import login, logout, authenticate, views as auth_views
from .forms import SignupForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token

from django.contrib.auth.models import Group
from django.core.mail import EmailMessage

from .models import CustomUser
from .signals import user_logged_in, user_logged_out, user_login_failed
from .utils import send_sms



HOST_EMAIL = 'subhajit.webkrone@gmail.com'


def redirect(args):
	return _redirect('accounts:'+str(args))



################ sign up ###################################################
def signup(request):    
	if request.method == 'POST':        
		#form = SignupForm(request.POST)
		agree = request.POST["agree"]  
		form = UserRegisterForm(request.POST)         
		if form.is_valid(): 
			if agree: 
				user = form.save(commit=False)   
				print('signup - user created...') 

				#user.is_active = False
				user.is_active = True
				user.save()
				print('signup - user saved...')

				current_site = get_current_site(request)
				user.send_verification_email(from_email=HOST_EMAIL)
				print('signup - verification email sent...')


				'''
				mail_subject = 'Activate your Account.' 
				"""           
				message = render_to_string('accounts/acc_active_email.html', {                
				'user': user,                
				'domain': current_site.domain,                
				'uid':urlsafe_base64_encode(force_bytes(user.pk)),                
				'token':account_activation_token.make_token(user),            
				})            
				"""
				message = f"""
				Hello {user.first_name},	
				Your account is created successfully!
				"""
				to_email = form.cleaned_data.get('email')            
				email = EmailMessage(mail_subject, message, to=[to_email])            
				email.send()
				'''

				request.session.flush()
				print('session flushed...')

				messages.success(request, f'You are successfully registered!!')
				print(f'You are successfully registered!!')
				#messages.info(request, f'Please verify your email address to get full access')
				#print( f'Please verify your email address to get full access')
				return redirect('login')

				#return HttpResponse('Please confirm your email address to complete the registration')

			else:
				messages.warning(request, f'Please check & agree to all Terms & Conditions')
				print(f'Please check & agree to all Terms & Conditions')
				return redirect('signup')

		else:
			messages.error(request, f'Invalid Entry, Please try again!')
			print(f'Invalid Entry, Please try again!')
			return redirect('signup')
			#return HttpResponse('Invalid Entry, Please try again!')
		 
	form = UserRegisterForm()
	return render(request, 'accounts/signup.html', {'form': form})




########################## sign up lite ###################################################
def signuplite(request):   
	try: 
		if request.method == 'POST':
			agree = request.POST["agree"]        
			form = UserRegisterLiteForm(request.POST)         
			
			print(agree)

			if form.is_valid():            
				if agree:
					user = form.save(commit=False)
					print('signuplite - user created...') 


					#user.is_active = False
					user.is_active = True
					user.save()
					print('signuplite - user saved...')

					current_site = get_current_site(request)

					request.session.flush()
					print('session flushed...')

					#login(request, user)
					#print('signup - user logged in...')

					messages.success(request, f'You are successfully registered!!')
					print(f'You are successfully registered!!')
					return redirect('login')
					#return HttpResponse('You are successfully registered!!')

				else:
					messages.warning(request, f'Please check & agree to all Terms & Conditions')
					print(f'Please check & agree to all Terms & Conditions')
					return redirect('signuplite')

			else:
				messages.error(request, f'Invalid Entry, Please try again!')
				print(f'Invalid Entry, Please try again!')
				return redirect('signuplite')
				#return HttpResponse('Invalid Entry, Please try again!')

	except Exception as err:
		messages.warning(request, f'Please check  & agree to all Terms & Conditions')
		print(f'Please check & agree to all Terms & Conditions')


	form = UserRegisterLiteForm()
	return render(request, 'accounts/signuplite.html', {'form': form})



  
############################# login view ###################################################
def login_view(request):
	if request.method == 'POST':
  
		# AuthenticationForm_can_also_be_used__

		email = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, email= email, password = password)
		if user is not None:
			form = login(request, user)
			print(f' Welcome {user.email} !!')
			messages.success(request, f' Welcome {user.email} !!')
			#return redirect('admin_dashboard')
			return redirect('user_dashboard')
		else:
			print(f'Access Denied: Invalid entry / Account does not exist')
			messages.error(request, f'Invalid entry / Account does not exist')
			return redirect('login')

	#form = AuthenticationForm()
	form = LoginForm()
	return render(request, 'accounts/login.html', {'form':form, 'title':'log in'})


"""
def login_view(request):
	if request.method == 'POST':
		m = CustomUser.objects.get(email=request.POST['email'])
		if m.password == m.get_password(request.POST['password']):
			request.session['member_id'] = m.id
			return HttpResponse("You're logged in.")
		else:
			return HttpResponse("Your username and password didn't match.")

	form = LoginForm()
	return render(request, 'accounts/login.html', {'form':form, 'title':'log in'})
"""



################ logout ###################################################
def logout(request):
	"""
		Remove the authenticated user's ID from the request and flush their session
		data.
	"""
	# Dispatch the signal before the user is logged out so the receivers have a
	# chance to find out *who* logged out.
	user = getattr(request, 'user', None)

	if not getattr(user, 'is_authenticated', True):
		user = None
	user_logged_out.send(sender=user.__class__, request=request, user=user)  # Custom pre logged_out signal
	request.session.flush()
	if hasattr(request, 'user'):
		from django.contrib.auth.models import AnonymousUser
		request.user = AnonymousUser()

	param = {}
	return render(request, 'accounts/logout.html', param)



######################## password change ###################################################
'''
def password_change(request):
	if request.method == 'POST':
  
		# AuthenticationForm_can_also_be_used__
  
		email = request.POST['username']
		password = request.POST['old_password']
		user = authenticate(request, email= email, password = password)
		if user is not None:

			new_password = request.POST['password']
			user.set_password(new_password)
			user.save()
			update_session_auth_hash(request,user)

			print( f' Password changed successfully !!')
			messages.success(request, f' Password changed successfully !!')
			return redirect('login')
		else:
			print(f' Account does not exist - Invalid Entry')
			messages.error(request, f'Account does not exist - Invalid Entry ')

	form = PasswordChangeForm()
	return render(request, 'accounts/password_reset.html', {'form':form, 'title':'Password Change'})

'''

def password_change(request):
	user = request.user
	if (hasattr(user, 'email')):

		if request.method == 'POST':
			try:
				form = PasswordChangeForm(user, request.POST)
				if form.is_valid():
					user = form.save()
					update_session_auth_hash(request,user)

					print(f' Password changed successfully !!')
					messages.success(request, f' Password changed successfully !!')
					return redirect('login')
				else:
					print(f'Invalid Entry - Try Again!')
					messages.error(request, f'Invalid Entry - Try Again!')
					return redirect('password_change')
					
			except Exception as err:
				print(f'Invalid Entry - {err}')
				messages.error(request, f'Invalid Entry - {err}')
				return redirect('password_change')

		form = PasswordChangeForm(user)
		return render(request, 'accounts/password_reset.html', {'form': form, 'title': 'Password Change'})

	print(f'You are not authorised - Please Log In!')
	messages.warning(request, f'You are not authorised - Please Log In!')
	return redirect('login')




################ Admin Dashboard ###################################################
#@login_required
def admin_dashboard(request):

	user = request.user
	print("USER IS : ", user)

	try:
		if user.email is not None:

			if not user.email_verified:
				messages.info(request, f'Please verify your email address to get full access')
				print( f'Please verify your email address to get full access')

			if user.is_superuser:
				print("Superuser")
				groups = Group.objects.all()
				users = CustomUser.objects.all()
				param ={
					'groups' : groups,
					'users'  : users,
					'user'   : user,
				 }  # Group, CustomUser, user
				return render(request, 'accounts/admin_dashboard.html', param)
			else:
				print("You are not superuser")
				return redirect('user_dashboard')
		
		print(f'Error: Account Email does not exit!')	
		messages.error(request, f'Error: Account Email does not exit!')
		return redirect('login')

	except Exception as err:
		print(f'Error: {err}, Please Try again!')	
		messages.error(request, f'Error: {err}, Please Try again!')
		return redirect('login')
	
	print(f'Account does not exit Plz Log In')		
	messages.error(request, f'Account does not exit Plz Log In')
	return redirect('login')



################ User Dashboard ###################################################
#@login_required
def user_dashboard(request):

	user = request.user
	print("USER IS : ", user)

	try:
		if user.email is not None:

			if user.is_active:
				print("User is_active")
				param ={
					'user'   : user,
				 }  
				return render(request, 'accounts/user_dashboard.html', param)
			else:
				print("User is not active")
				messages.warning(request, f'User is not active')
				return redirect('login')
				
		print(f'Error: Account Email does not exit!')	
		messages.error(request, f'Error: Account Email does not exit!')
		return redirect('login')

	except Exception as err:
		print(f'Error: {err}, Please Try again!')	
		messages.error(request, f'Error: {err}, Please Try again!')
		return redirect('login')
	
	print(f'Account does not exit Plz Log In')		
	messages.error(request, f'Account does not exit Plz Log In')
	return redirect('login')




from django.contrib.auth import  get_user
############################# Verify User by Email OTP ##########################################
def verify_email_view(request):
	user = request.user
	#user = get_user(request)
	try:
		if user.email is not None:

			if request.method == 'POST':
				token = request.POST['otp']
				response = user.verify_email(token)
				print(user)

				if (response == True):
					print(f'Congrats!! You are successfully verified')
					messages.success(request, f'Congrats!! You are successfully verified')
					#return redirect('user_dashboard')
					return redirect('admin_dashboard')

				elif (response == False):
					print(f'Error - Please Enter valid OTP')
					messages.error(request, f'Error - Please Enter valid OTP')
					return redirect('verify_email')

				elif (response == None):
					print(f'Error- This OTP is expired! Check Your Email for new OTP')
					user.send_verification_email(from_email=HOST_EMAIL, validity=10)
					messages.error(request, f'Error- This OTP is expired! Check Your Email for new OTP')
					print(f'New OTP sent.')
					return redirect('verify_email')

			return render(request, 'accounts/verify_email.html')

	except:
		print('except')
		pass

	print(f'Please Login before Email verification!')
	messages.warning(request, f'Please Login before Email verification!')
	return redirect('login')




############################# SEND PHONE OTP ##########################################
def send_email_otp(request):
	user = request.user
	#user = get_user(request)
	try:
		if user.email is not None:
			print(f'{user.email}')
			token_validity = 10 	# validity of token (default 10 minutes.)
			auth_token = user.create_email_token(duration=token_validity, token_len=6, token_type='numeric')
			token = auth_token.token

			message = f"Hello {user.get_full_name()}, \nOTP : {token} to verify your Email. \
			 \nThis OTP is valid for {token_validity} minutes only.\nTeam WebKrone." 

			user.send_verification_email(from_email=HOST_EMAIL, validity=token_validity, message=message, auth_token=auth_token)

			print(f'Check your email to get the OTP')
			messages.info(request, f'Check your email to get the OTP')
			return redirect('verify_email')


	except Exception as err:
		print(f'Error-{err}')

	print(f'You are not Registered- Please Log In!')
	messages.warning(request, f'You are not Registered- Please Log In!')
	return redirect('login')




############################# Verify User by Phone OTP ##########################################
def verify_phone_view(request):
	user = request.user
	#user = get_user(request)
	try:
		if user.email is not None:

			if request.method == 'POST':
				token = request.POST['otp']
				response = user.verify_ph(token)
				print(user)

				if (response == True):
					print(f'Congrats!! Your phone number is successfully verified')
					messages.success(request, f'Congrats!! Your phone number is successfully verified')
					#return redirect('user_dashboard')
					return redirect('admin_dashboard')

				elif (response == False):
					print(f'Error - Please Enter valid OTP')
					messages.error(request, f'Error - Please Enter valid OTP')
					return redirect('verify_phone')

				elif (response == None):
					print(f'Error- This OTP is expired! Check Your phone for new OTP')
					messages.error(request, f'Error- This OTP is expired! Check Your phone for new OTP')
					print(f'Sending New OTP ...')
					return redirect('send_phone_otp')

			return render(request, 'accounts/verify_phone.html')

	except Exception as err:
		print(f'Error-{err}')


	print(f'Please Login before phone number verification!')
	messages.warning(request, f'Please Login before phone number verification!')
	return redirect('login')



############################# SEND PHONE OTP ##########################################
def send_phone_otp(request):
	user = request.user
	#user = get_user(request)
	try:
		if user.email is not None:
			print(f'{user.email}')
			if user.ph_no:

				print(f'{user.ph_no}')
				token_validity = 10
				auth_token = user.create_ph_token(duration=token_validity, token_len=6, token_type='numeric')
				token = auth_token.token

				message = f"Hello {user.get_full_name()}, \nOTP : {token} to verify your phone number. \
				 \nOTP is valid for {token_validity} minutes only.\nTeam WebKrone."

				send_sms(message=message, number=user.ph_no)

				print(f'Check your phone to get the OTP')
				messages.info(request, f'Check your phone to get the OTP')
				return redirect('verify_phone')

			else:
				print(f'Your phone number is not registered, Enter Your Ph. Number and try again!')
				messages.warning(request, f'Your phone number is not registered, Enter Your Ph. Number and try again!')
				return redirect('user_dashboard')

	except Exception as err:
		print(f'Error-{err}')

	print(f'You are not Registered- Please Log In!')
	messages.warning(request, f'You are not Registered- Please Log In!')
	return redirect('login')




################ password Forget/Reset ###################################################
def password_forget(request):

	if request.method == 'POST':
		try:
			form = accounts_forms.PasswordForgetForm(request.POST)
			if form.is_valid():

				email = request.POST['email']
				request.session['email'] = email
				print("Email saved in session!")

				user = CustomUser.objects.get(email=email)
				token_validity = 10
				auth_token = user.create_email_token(token_len=10, duration=token_validity)
				token = auth_token.token
				print("Token Created for verification")

				link = f'http://127.0.0.1:8000/password_reset/{token}'
				link2 = f'http://127.0.0.1:8000/password_reset_otp'
				subject = "Reset Your Password"
				message = f"""
				Hello {user.get_full_name()},

				Please visit this link to reset your password.
				{link}
					
				OR,
				Use OTP : {token}
				{link2}

				NOTE: This link is valid for {token_validity} minutes only.

				Team WebKrone.
				"""
				user.send_verification_email(subject, message, from_email=HOST_EMAIL, auth_token=auth_token)

				print(f'Check your Email to reset password!')
				messages.info(request, f'Check your Email to reset password!')
				return redirect('password_reset_pending')

		except Exception as err:
			print(f'Invalid - {err}')
			messages.error(request, f'Invalid - {err}')
			return redirect('password_forget')

	form = accounts_forms.PasswordForgetForm()
	return render(request, 'accounts/password_forget.html', {'form': form, 'title': 'Password Reset'})




####################################################################
def password_reset_pending(request):

	try:
		email = request.session['email']
		print(f"Email taken from session! - {email}")

		user = CustomUser.objects.get(email=email)
		print(f"User taken from Database! - {user}")

		if (hasattr(user, 'email')):
			return render(request, 'accounts/password_reset_pending.html')

	except Exception as err:
		print(f"Exception- {err}")

	print(f'You are not authorised to access the page!')
	messages.warning(request, f'You are not authorised to access the page!')
	return redirect('password_forget')




####################################################################
def password_reset_by_link(request, token=''):

	try:
		email = request.session['email']
		print(f"Email taken from session! - {email}")

		user = CustomUser.objects.get(email=email)
		print(f"User taken from Database! - {user}")

		if (hasattr(user, 'email')):

			auth_token = user.get_token(email_verification=True)
			if auth_token is not None:

				if auth_token.token == token:
					print(f"User token matched! - {token}")

					request.session['token'] = token

					print(f'Verification Successfull!!')
					messages.success(request, f'Verification Successfull!!')
					return redirect('password_reset')

				print(f'Invalid Link- Try Again!!')
				messages.error(request, f'Invalid Link- Try Again!!')
				return redirect('password_forget')

			print(f'Link is expired- Try Again!!')
			messages.error(request, f'Link is expired - Try Again!!')
			return redirect('password_forget')

	except Exception as err:
		print(f"Exception- {err}")

	print(f'You are not authorised to access the page!')
	messages.warning(request, f'You are not authorised to access the page!')
	return redirect('password_forget')




####################################################################
def password_reset_by_otp(request):

	try:
		email = request.session['email']
		print(f"Email taken from session! - {email}")

		user = CustomUser.objects.get(email=email)
		print(f"User taken from Database! - {user}")

		if (hasattr(user, 'email')):
			if request.method == 'POST':
				token = request.POST['otp']

				auth_token = user.get_token(email_verification=True)
				if auth_token is not None:

					if auth_token.token == token:
						print(f"User token matched! - {token}")

						request.session['token'] = token

						print(f'Verification Successfull!!')
						messages.success(request, f'Verification Successfull!!')
						return redirect('password_reset')

					print(f'Invalid OTP- Try Again!!')
					messages.error(request, f'Invalid OTP- Try Again!!')

				print(f'OTP is expired- Try Again!!')
				messages.error(request, f'OTP is expired - Try Again!!')
				return redirect('password_forget')

			########
			return render(request, 'accounts/password_reset_by_otp.html')

	except Exception as err:
		print(f"Exception- {err}")

	print(f'You are not authorised to access the page!')
	messages.warning(request, f'You are not authorised to access the page!')
	return redirect('password_forget')



####################################################################
def password_reset(request):

	try:
		email = request.session['email']
		print(f"Email taken from session! - {email}")

		user = CustomUser.objects.get(email=email)
		print(f"User taken from Database! - {user}")

		token = request.session['token']
		print(f"Token taken from session! - {token}")

		if (hasattr(user, 'email')):
			auth_token = user.get_token(email_verification=True)
			if auth_token is not None:
				if auth_token.token == token:
					print(f"User token matched! - {token}")

					if request.method == 'POST':
						form = SetPasswordForm(user, request.POST)
						print("form created -POST")
						if form.is_valid():
							user = form.save()
							request.session.flush()
							user.delete_token(email_verification=True)

							print(f' Password reset successfully !!')
							messages.success(request, f' Password reset successfully !!')
							return redirect('login')

						else:
							print(f'Invalid Entry - Try Again!')
							messages.error(request, f'Invalid Entry - Try Again!')
							return redirect('password_reset')

					form = SetPasswordForm(user)
					print("form created -GET")
					return render(request, 'accounts/password_reset.html', {'form': form, 'title': 'Password Reset'} )

				print(f'Invalid Link- Try Again!!')
				messages.error(request, f'Invalid Link- Try Again!!')

			print(f'Link is expired- Try Again!!')
			messages.error(request, f'Link is expired - Try Again!!')
			return redirect('password_forget')

	except Exception as err:
		print(f"Exception- {err}")

	print(f'You are not authorised to access the page!')
	messages.warning(request, f'You are not authorised to access the page!')
	return redirect('password_forget')


# Update User details:
def user_update(request):
	#################### Checking User Log In: ##########################
	FAILED = False
	user = request.user
	try:
		if user.email is None:
			FAILED = True
	
	except Exception as err:
		print(f"ErrorType- {type(err)}")
		print(f"Error- {err}")
		
		FAILED = True
	
	if FAILED:
		messages.warning(request, f"Please Login to access the page")
		print(f"Please Login to access the page")
	
	else:
		print(f"Get user :{user}")
		
		if request.method == "POST":
			# user.first_name = request.POST['first_name']
			# user.last_name = request.POST['last_name']
			# user.username = request.POST['username']
			# user.ph_no = request.POST['ph_no']
			
			form = UserUpdateForm(data=request.POST, instance=request.user)
			if form.is_valid():
				form.save()
			else:
				messages.warning(request, f"Invalid Details: Username & Phone number must be unique.")
				print(f"Invalid Details: Username & Phone number must be unique.")
			
	# Returns None if user came from another website
	url = request.META.get('HTTP_REFERER')
	print(f"Redirecting to - {url}")
	
	if url is not None:
		return redirect(url)
	return redirect('user_dashboard')
	

# Error
def error404(request, exception):
	return render(request, "errors/404.html")


def error500(request):
	return render(request, "errors/500.html")