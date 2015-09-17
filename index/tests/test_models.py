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

    def test_celery(self):
        # test celery
        project = Project(
            name='Test',
            slug='test',
            description='test description'
        )
        # ensure get dependencies works as expected
        # if no repository is given
        promise = project.get_dependencies()
        while not promise.ready():
            time.sleep(1)
        self.assertEqual(promise.result, False)

        # ensure get_readme works as expected
        # if no repository is given
        promise = project.get_readme()
        while not promise.ready():
            time.sleep(1)
        self.assertEqual(promise.result, False)

        project.save()
        # a repo with a readme.md and requirements.txt
        Repository(
            name='github',
            url='https://github.com/grnet/project_index.git',
            project=project
        ).save()

        # ensure get dependencies works as expected
        # if no repository is given
        promise = project.get_dependencies()
        while not promise.ready():
            time.sleep(1)
        self.assertEqual(promise.result, True)

        # ensure get_readme works as expected
        # if no repository is given
        promise = project.get_readme()
        while not promise.ready():
            time.sleep(1)
        self.assertEqual(promise.result, True)
