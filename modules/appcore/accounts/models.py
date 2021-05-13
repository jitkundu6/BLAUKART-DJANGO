from django.db import models
from django.contrib.auth.models import AbstractBaseUser, User, AbstractUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from .managers import CustomUserManager

from django.contrib.auth.validators import UnicodeUsernameValidator

from django.utils.timezone import timedelta
from .utils import get_otp

from django.core.mail import send_mail

HOST_EMAIL = 'subhajit.webkrone@gmail.com'


class CustomUser(AbstractBaseUser, PermissionsMixin):
	"""
	Custom User class implementing a fully featured User model with
	managers-compliant permissions.

	Email and password are required. Other fields are optional.
	"""
	ph_no = models.CharField(max_length=15, unique=True, null=True)
	last_updated = models.DateTimeField(auto_now=True)
	
	# verified = models.BooleanField(default=False)
	ph_verified = models.BooleanField(default=False)
	email_verified = models.BooleanField(default=False)
	
	username_validator = UnicodeUsernameValidator()
	
	username = models.CharField(
		_('username'),
		max_length=150,
		unique=True,
		help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
		validators=[username_validator],
		error_messages={
			'unique': _("A user with that username already exists."),
		},
		null=True,
		blank=True,
	)
	
	first_name = models.CharField(_('first name'), max_length=150, blank=True)
	last_name = models.CharField(_('last name'), max_length=150, blank=True)
	email = models.EmailField(_('email address'), unique=True)
	is_staff = models.BooleanField(
		_('staff status'),
		default=False,
		help_text=_('Designates whether the user can log into this managers site.'),
	)
	
	is_active = models.BooleanField(
		_('active'),
		default=True,
		help_text=_(
			'Designates whether this user should be treated as active. '
			'Unselect this instead of deleting accounts.'
		),
	)
	date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
	
	objects = CustomUserManager()
	
	class Meta(AbstractUser.Meta):
		verbose_name = _('user')
		verbose_name_plural = _('users')
		# abstract = True
		swappable = 'AUTH_USER_MODEL'
	
	EMAIL_FIELD = 'email'
	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['username']
	
	def __str__(self):
		return self.email
	
	def clean(self):
		super().clean()
		self.email = self.__class__.objects.normalize_email(self.email)
	
	def get_full_name(self):
		"""
		return: first_name plus last_name, with a space in between.
		"""
		full_name = '%s %s' % (self.first_name, self.last_name)
		return full_name.strip()
	
	def get_short_name(self):
		"""
		return: first name as short name of the user.
		"""
		return self.first_name
	
	def email_user(self, subject, message, from_email=HOST_EMAIL, **kwargs):
		"""
		Send an email to this user.
		:param subject: Subject of the email
		:param message: Body of the email
		:param from_email: Email sender
		:return: True if email sent successfully
				 False if email sending failed
		"""
		try:
			send_mail(subject, message, from_email, [self.email], **kwargs)
			print("---Email sent to user.")
			return True
		except Exception as err:
			print(f"email_user() Error - {err}")
			print("---Email is not sent to user.")
			return False
	
	def check_token_expiry(self, ph_verification=False, email_verification=False):
		"""
		Check Expiry of Token:
		Return True if Token is Expired otherwise False.
		Return None if Token is not available.
		"""
		try:
			auth_token = AuthToken.objects.get(user=self, ph_verification=ph_verification,
			                                   email_verification=email_verification)
			if (auth_token.created + auth_token.duration < timezone.now()):
				auth_token.delete()
				return True
			return False
		
		except:
			pass
		
		return None
	
	def get_token(self, ph_verification=False, email_verification=False):
		"""
		Search for Token for Phone/ Email Verification based on passed parameters.
		Return 'None' if Token is not available/ expired
		Return the Token object if available.
		"""
		try:
			auth_token = AuthToken.objects.get(user=self, ph_verification=ph_verification,
			                                   email_verification=email_verification)
			
			if (auth_token is None):
				return None
			
			if (auth_token.created + auth_token.duration < timezone.now()):
				auth_token.delete()
				return None
			
			return auth_token
		
		except:
			# Exception occur when Multiple / No Token available.
			try:
				# if multiple token available, then delete all previous tokens.
				auth_tokens = AuthToken.objects.filter(user=self, ph_verification=ph_verification,
				                                       email_verification=email_verification)
				auth_tokens[0].delete()
				return self.get_token(ph_verification, email_verification)
			except:
				# if no token available, then return None.
				return None
	
	def delete_token(self, ph_verification=False, email_verification=False):
		"""
		Delete the Token for Phone/ Email Verification based on passed parameters.
		Return 'True' if Token is successfully deleted.
		Return 'False' if Token is not available.
		"""
		try:
			auth_token = self.get_token(self, ph_verification=ph_verification, email_verification=email_verification)
			auth_token.delete()
			return True
		except Exception as err:
			print(f"delete_token() Error - {err}")
			return False
	
	def create_token(self, duration=10, token_len=6, token_type='numeric', ph_verification=False,
	                 email_verification=False):
		"""
		Create a new Auth Token:
		:param duration: Token validity (in Minutes)
		:param token_len: Length of the Token.
		:param token_type: Type of Token ( 'numeric' / 'alpha' / 'alpha-numeric' )
		:return: AuthToken objects
		"""
		
		# Delete if any old token with same details available and create a new one.
		try:
			auth_token = self.get_token(ph_verification=ph_verification, email_verification=email_verification)
			if auth_token is not None:
				auth_token.delete()
			
			auth_token = AuthToken(user=self, ph_verification=ph_verification, email_verification=email_verification)
		
		except:
			auth_token = AuthToken(user=self, ph_verification=ph_verification, email_verification=email_verification)
		
		# Token length Constrain 4 - 30
		if (token_len < 4):
			token_len = 4
		if (token_len > 30):
			token_len = 30
		
		# Token type selection (Numeric/ Alphabetic/ Alpha-Numeric)
		if (token_type == 'numeric'):
			auth_token.token = get_otp(token_len, 1234567890)
		elif (token_type == 'alpha'):
			auth_token.token = get_otp(token_len, "qwertyuiopasdfghjklzxcvbnm")
		elif (token_type == 'alpha-numeric'):
			auth_token.token = get_otp(token_len, "1234567890QWERTYUIOPASDFGHJKLZXCVBNM")
		else:
			auth_token.token = get_otp(token_len)
		
		# Setting the duration of Auth Token
		auth_token.duration = timedelta(0, 60 * duration)
		auth_token.save()
		
		return auth_token
	
	def create_email_token(self, duration=10, token_len=6, token_type='alpha-numeric'):
		"""
		Create a new Auth Token for email varification.
		:param duration: Token validity (in Minutes)
		:param token_len: Length of the Token.
		:param token_type: Type of Token ( 'numeric' / 'alpha' / 'alpha-numeric' )
		:return: AuthToken objects
		"""
		auth_token = self.create_token(duration, token_len, token_type, email_verification=True)
		# auth_token.email_verification = True
		auth_token.save()
		return auth_token
	
	def create_ph_token(self, duration=10, token_len=6, token_type='alpha-numeric'):
		"""
		Create a new Auth Token for phone number varification.
		:param duration: Token validity (in Minutes)
		:param token_len: Length of the Token.
		:param token_type: Type of Token ( 'numeric' / 'alpha' / 'alpha-numeric' )
		:return: AuthToken objects
		"""
		auth_token = self.create_token(duration, token_len, token_type, ph_verification=True)
		# auth_token.ph_verification = True
		auth_token.save()
		return auth_token
	
	def verify_ph(self, token):
		"""
		Verify this User's Phone Number:
		Return True if Token is Verified otherwise False.
		Return None if Token is not available.
		"""
		auth_token = self.get_token(ph_verification=True)
		
		if auth_token is None:
			return None
		
		if (auth_token.token == token):
			self.ph_verified = True
			self.save()
			auth_token.delete()
			return True
		else:
			return False
	
	def verify_email(self, token):
		""" Verify this User's Email:
		Return True if Token is Verified otherwise False.
		Return None if Token is not available.
		"""
		auth_token = self.get_token(email_verification=True)
		
		if auth_token is None:
			return None
		
		if (auth_token.token == token):
			self.email_verified = True
			self.save()
			auth_token.delete()
			return True
		else:
			return False
	
	def send_verification_email(self, subject="", message="", from_email=None, auth_token=None, validity=10, **kwargs):
		"""
		Send verification email to this user.
		:param subject: Subject of the email
		:param message: Body of the email
		:param from_email: Email sender
		:param auth_token: AuthToken object to get the token for verification email
		:param validity: Validity/ Duration of token
		:return: True if email sent successfully
				 False if email sending failed
		"""
		print("---Sending Verification Email!")
		
		if auth_token is None:
			auth_token = self.create_email_token(duration=validity, token_len=6, token_type='alpha-numeric')
		
		if subject == '':
			subject = "Verify Your Account"
		
		if message == '':
			message = f"""
Hello {self.get_full_name()},

Please use this OTP to verify your account.
OTP : {auth_token.token}

NOTE: This OTP is valid for {validity} minutes only.

Team WebKrone.
                """
		return self.email_user(subject, message, from_email, **kwargs)


# Verification Token Model
class AuthToken(models.Model):
	user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
	token = models.CharField(max_length=50, default=get_otp(6))
	created = models.DateTimeField(default=timezone.now)
	duration = models.DurationField(default=timedelta(0, 600))  # default duration 10 mins
	# verified = models.BooleanField(default=False)
	ph_verification = models.BooleanField(default=False)
	email_verification = models.BooleanField(default=False)
	
	def __str__(self):
		if (self.ph_verification and not self.email_verification):
			token_for = "Phone OTP"
		elif (not self.ph_verification and self.email_verification):
			token_for = "Email OTP"
		else:
			token_for = "Invalid OTP"
		
		return str(self.id) + " : " + self.user.email + " : " + token_for
