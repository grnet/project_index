from django.test import TestCase
from index.models import Project, Repository
import time


class IndexTest(TestCase):

    def test_insert_project(self):
        # create an object for each model
        project = Project(
            name='Test',
            slug='test',
            description='test description'
        )
        project.save()

