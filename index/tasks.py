from __future__ import absolute_import
import os
import random
import string
from celery import shared_task
from gittle import Gittle
import shutil


def parse_dependencies(line, project):
    version = ''
    name = ''
    if '==' in line:
        name = line.split('==')[0]
        version = line.split('==')[1]
    else:
        name = line
    if name:
        from index.models import Dependency
        (dep, created) = Dependency.objects.get_or_create(
            name=name.split('/')[-1].strip(),
            version=version.strip(),
            pip_package_name=name.strip()
        )
        project.dependencies.add(dep)
    return True


@shared_task
def get_requirements(project):
    repos = project.repository_set.all()
    if repos:
        for repository in repos:
            if repository.url:
                path = ('/tmp/%s/') % ''.join(random.choice(string.lowercase) for i in range(20))
                try:
                    repo = Gittle.clone(repository.url, path, bare=True)
                except:
                    pass
                else:
                    requirements = repo.file_versions('requirements.txt')
                    if requirements:
                        requirements = requirements[0].get('data')
                        for r in requirements.split('\n'):
                            parse_dependencies(r, project)
                        shutil.rmtree(repo.path)
                        return True
    if project.dependency_file:
        if os.path.isfile(project.dependency_file.path):
            for l in project.dependency_file.readlines():
                parse_dependencies(l, project)
            return True
    return False


@shared_task
def get_readme(project):
    '''
    This function tries to get the content of the readme file. If it does, then
    it updates the description with the content of the latest readme. It runs
    every time a project is saved, on post save hook.
    '''
    repos = project.repository_set.all()
    if repos:
        for repository in repos:
            if repository.url:
                path = ('/tmp/%s/') % ''.join(random.choice(string.lowercase) for i in range(20))
                try:
                    repo = Gittle.clone(repository.url, path, bare=True)
                except:
                    pass
                else:
                    readme = repo.file_versions('README.md')
                    if readme:
                        readme = readme[0].get('data')
                        # We use update, because we want to bypass
                        # the post_save function.
                        from index.models import Project
                        Project.objects.filter(id=project.id).update(description=readme)
                        shutil.rmtree(repo.path)
                        return True
    return False
