from __future__ import unicode_literals
import bcrypt

from django.db import models
import re

class UserManager(models.Manager):
	def register(self, data):
		errors = []
		EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
		first_regex = re.compile(r'^.[a-zA-Z]')
		last_regex = re.compile(r'^.[a-zA-Z]')

		if not data["first_name"]:
			errors.append("First name field blank")

		if len(data["first_name"]) < 2:
			errors.append("First name field cannot be less than 2 characters")

		if not re.search(first_regex, data["first_name"]):
			errors.append("First name must be only letters")

		if not data["last_name"]:
			errors.append("Last name field blank")

		if len(data["last_name"]) < 2:
			errors.append("Last name field cannot be less than 2 characters")

		if not re.search(last_regex, data["last_name"]):
			errors.append("Last name must be only letters")

		if not data["password"]:
			errors.append("Password field blank")

		if len(data["password"]) < 6:
			errors.append("Password field cannot be less than 6 characters")

		if not data["password"] == data["confirm_password"]:
			errors.append("Passwords do not match")

		Epassword = data['password']
		hashedpass = bcrypt.hashpw(Epassword.encode(), bcrypt.gensalt())

		if not data ["email"]:
			errors.append("Email field blank")

		if not EMAIL_REGEX.match(data['email']):
			errors.append("Must be valid email")
		
		else:
			existing_email = self.filter(email=data["email"])

			if existing_email:
				errors.append("Email already exists.")



		response = {}

		if errors:
			response["created"] = False
			response["errors"] = errors

		else:
			hashedpass = bcrypt.hashpw(Epassword.encode(), hashedpass.encode())
			new_user = Users.objects.create(first_name = data["first_name"],last_name = data["last_name"], email=data["email"], password = hashedpass)
			response["created"] = True
			response["new_user"] = new_user
	

		return response

	def login (self, data):
		errors = []
		EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
		response = {}
		existing_email= Users.objects.filter(email=data['email'])
		existing_password = Users.objects.filter(password=data['password'])

		if not data['email']:
			errors.append("Email field blank")

		if not data['password']:
			errors.append("Password field blank")

		if not existing_email:
			errors.append("Email not recognized")

		if not existing_password:
			errors.append("Password not recognized")

		if existing_email:

			if existing_password:
				response["created"] = True


		else:
			errors.append("Username or Email not recognized")

		response = {}

		if errors:
			response["created"] = False
			response["errors"] = errors


		else:
			response["created"] = False
			response["errors"] = errors
				
		return response


class Users(models.Model):
	first_name = models.CharField(max_length=45)
	last_name = models.CharField(max_length=45)
	email = models.CharField(max_length=100)
	password = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)

	objects = UserManager()
