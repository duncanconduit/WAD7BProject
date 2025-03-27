
import os
import re
import json
import inspect
import tempfile
import accounts.models
import templates
#from rango import forms
#from populate_rango import populate
#from populate_script import populate
from accounts.models import User, Organisation
from templates import accounts
from django.db import models
from django.test import TestCase
from django.conf import settings
from django.urls import reverse, resolve
#from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.forms import fields as django_fields


FAILURE_HEADER = f"{os.linesep}{os.linesep}{os.linesep}================{os.linesep}TwD TEST FAILURE =({os.linesep}================{os.linesep}"
FAILURE_FOOTER = f"{os.linesep}"

class test_accounts(TestCase):
    
    def test_user_str(self):
            # Create a User instance
            User=get_user_model()
            self.organisation = Organisation.objects.create(name="Test Organisation")
            user = User.objects.create_user(
                email="alice@example.com", 
                first_name="Alice", 
                last_name="Smith", 
                password="testpassword123", 
                organisation=self.organisation
            )

            # Test the string representation of the User
            self.assertEqual(str(user), "alice@example.com")

    def create_user_object(self):
        
        #Helper function to create a User object.
        User=get_user_model()
        user = User.objects.get_or_create(email='alice@example.com',
                                        first_name='Alice',
                                        last_name='Smith'
                                        )[0]
        user.set_password('testpassword123')
        user.save()

        return user

    #def test_unregistered_user_cannot_access_meetings(self):

    def test_login_functionality(self):
        
        #Tests the login functionality. A user should be able to log in, and should be redirected to the dashboard.
        
        user_object = self.create_user_object()

        response = self.client.post(reverse('accounts:login'), {'email': 'alice@example.com', 'password': 'testpassword123'})
        response_data = json.loads(response.content)
        try:
            self.assertEqual(user_object.id, int(self.client.session['_auth_user_id']), f"{FAILURE_HEADER}We attempted to log a user in with an ID of {user_object.id}, but instead logged a user in with an ID of {self.client.session['_auth_user_id']}. Please check your login() view.{FAILURE_FOOTER}")
        except KeyError:
            self.assertTrue(False, f"{FAILURE_HEADER}When attempting to log in with your login() view, it didn't seem to log the user in. Please check your login() view implementation, and try again.{FAILURE_FOOTER}")

        self.assertEqual(response.status_code, 200, f"{FAILURE_HEADER}Testing your login functionality, logging in was successful. However, we expected a redirect; we got a status code of {response.status_code} instead. Check your login() view implementation.{FAILURE_FOOTER}")
        self.assertEqual(response_data['redirect'], reverse('dashboard:index'), f"{FAILURE_HEADER}We were not redirected to the Rango homepage after logging in. Please check your login() view implementation, and try again.{FAILURE_FOOTER}")

    def test_good_request(self):
        """
        Attempts to log out a user who IS logged in.
        This should succeed -- we should be able to login, check that they are logged in, logout, and perform the same check.
        """
        user_object = self.create_user_object()
        self.client.login(email='alice@example.com', password='testpassword123')

        try:
            self.assertEqual(user_object.id, int(self.client.session['_auth_user_id']), f"{FAILURE_HEADER}We attempted to log a user in with an ID of {user_object.id}, but instead logged a user in with an ID of {self.client.session['_auth_user_id']}. Please check your login() view. This happened when testing logout functionality.{FAILURE_FOOTER}")
        except KeyError:
            self.assertTrue(False, f"{FAILURE_HEADER}When attempting to log a user in, it failed. Please check your login() view and try again.{FAILURE_FOOTER}")
        
        # Now lot the user out. This should cause a redirect to the homepage.
        response = self.client.get(reverse('accounts:logout'))
        self.assertEqual(response.status_code, 302, f"{FAILURE_HEADER}Logging out a user should cause a redirect, but this failed to happen. Please check your logout() view.{FAILURE_FOOTER}")
        self.assertEqual(response.url, reverse('dashboard:index'), f"{FAILURE_HEADER}When logging out a user, the book states you should then redirect them to the homepage. This did not happen; please check your logout() view.{FAILURE_FOOTER}")
        self.assertTrue('_auth_user_id' not in self.client.session, f"{FAILURE_HEADER}Logging out with your logout() view didn't actually log the user out! Please check yout logout() view.{FAILURE_FOOTER}")



    def test_new_login_view_exists(self):
        """
        Checks to see if the new registration view exists in the correct place, with the correct name.
        """
        url = ''

        try:
            url = reverse('accounts:login')
        except:
            pass
        
        self.assertEqual(url, '/accounts/login/', f"{FAILURE_HEADER}Have you created the rango:register URL mapping correctly? It should point to the new register() view, and have a URL of '/rango/register/' Remember the first part of the URL (/rango/) is handled by the project's urls.py module, and the second part (register/) is handled by the Rango app's urls.py module.{FAILURE_FOOTER}")
    

    def test_new_registration_view_exists(self):
        """
        Checks to see if the new registration view exists in the correct place, with the correct name.
        """
        url = ''

        try:
            url = reverse('accounts:register')
        except:
            pass
        
        self.assertEqual(url, '/accounts/register/', f"{FAILURE_HEADER}Have you created the rango:register URL mapping correctly? It should point to the new register() view, and have a URL of '/rango/register/' Remember the first part of the URL (/rango/) is handled by the project's urls.py module, and the second part (register/) is handled by the Rango app's urls.py module.{FAILURE_FOOTER}")
"""
class Chapter9RestrictedAccessTests(TestCase):
    
    def test_bad_request(self):
        
        Tries to access the restricted view when not logged in.
        This should redirect the user to the login page.
        
        response = self.client.get(reverse('dashboard:index'))
        #response_data = json.loads(response.content)
        self.assertEqual(response.status_code, 200, f"{FAILURE_HEADER}We {response.status_code} tried to access the restricted view when not logged in. We expected to be redirected, but were not. Check your restricted() view.{FAILURE_FOOTER}")
        self.assertTrue(response["message"].startswith(reverse('accounts:login')), f"{FAILURE_HEADER}We tried to access the restricted view when not logged in, and were expecting to be redirected to the login view. But we were not! Please check your restricted() view.{FAILURE_FOOTER}")
       

    def test_good_request(self):
        
        Attempts to access the restricted view when logged in.
        This should not redirect. We cannot test the content here. Only links in base.html can be checked -- we do this in the exercise tests.
    
        
        user_object = self.create_user_object()
        self.client.login(email='alice@example.com', password='testpassword123')

        response = self.client.get(reverse('dashboard:index'))
        self.assertTrue(response.status_code, 200)
"""