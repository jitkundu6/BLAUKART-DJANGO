from django.db import models

# Create your models here.

class Contact(models.Model):
	name = models.CharField(max_length=30)
	email = models.EmailField()
	subject = models.CharField(max_length=100)
	message = models.TextField()
	phone =  models.CharField(max_length=20, blank=True)
	
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)