import os
import re
import inspect
import tempfile
from django.test import TestCase

import meetings.views
import meetings.urls
import importlib
from django.urls import reverse
from django.test import TestCase
from django.conf import settings
from .views import about,contact

