
import os
import re
import inspect
import tempfile
from django.test import TestCase

import eventio.views
import eventio.urls
import importlib
from django.urls import reverse
from django.test import TestCase
from django.conf import settings
from .views import about,contact


FAILURE_HEADER = f"{os.linesep}{os.linesep}{os.linesep}================{os.linesep}TwD TEST FAILURE =({os.linesep}================{os.linesep}"
FAILURE_FOOTER = f"{os.linesep}"


class test_eventio_about(TestCase):
    def setUp(self):
        self.views_module = importlib.import_module('eventio.views')
        self.views_module_listing = dir(self.views_module)
        self.response = self.client.get(reverse('about'))
        self.content = self.response.content.decode()

    def test_mapping_exists_about(self):
            """
            Checks whether the about view has the correct URL mapping.
            """
            self.assertEquals(reverse('about'), '/about/', f"{FAILURE_HEADER}Your about URL mapping is either missing or mistyped.{FAILURE_FOOTER}")


    def test_view_exists_about(self):
        
        name_exists = 'about' in self.views_module_listing
        is_callable = callable(self.views_module.about)
        
        self.assertTrue(name_exists, f"{FAILURE_HEADER}We couldn't find the view for your about view! It should be called about().{FAILURE_FOOTER}")
        self.assertTrue(is_callable, f"{FAILURE_HEADER}Check you have defined your about() view correctly. We can't execute it.{FAILURE_FOOTER}")
    
    def test_template_filename(self):
        self.assertTemplateUsed(self.response, 'about.html', f"{FAILURE_HEADER}Are you using about.html for your about() view? Why not?!{FAILURE_FOOTER}")

class test_eventio_contact(TestCase):

    def setUp(self):
            self.views_module = importlib.import_module('eventio.views')
            self.views_module_listing = dir(self.views_module)
            self.response = self.client.get(reverse('contact'))
            self.content = self.response.content.decode()
    
   
    def test_view_exists_contact(self):
        
        name_exists = 'contact' in self.views_module_listing
        is_callable = callable(self.views_module.contact)
        
        self.assertTrue(name_exists, f"{FAILURE_HEADER}We couldn't find the view for your about view! It should be called contact().{FAILURE_FOOTER}")
        self.assertTrue(is_callable, f"{FAILURE_HEADER}Check you have defined your contact() view correctly. We can't execute it.{FAILURE_FOOTER}")
    
    def test_mapping_exists_contact(self):
        """
        Checks whether the about view has the correct URL mapping.
        """
        self.assertEquals(reverse('contact'), '/contact/', f"{FAILURE_HEADER}Your about URL mapping is either missing or mistyped.{FAILURE_FOOTER}")
    
    def test_template_filename(self):
            self.assertTemplateUsed(self.response, 'contact.html', f"{FAILURE_HEADER}Are you using contact.html for your contact() view? Why not?!{FAILURE_FOOTER}")

