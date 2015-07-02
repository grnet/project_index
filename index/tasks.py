from __future__ import absolute_import
import random
import string
import os
from celery import shared_task
from gittle import Gittle


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
                    repo = Gittle.clone_(repository.url, path, bare=True)
                except:
                    # could not connect to the repo
                    continue
                else:
                    requirements = repo.file_versions('requirements.txt')
                    if requirements:
                        requirements = requirements[0].get('data')
                        for r in requirements.split('\n'):
                            parse_dependencies(r, project)
                        os.rmdir(repo.path)
                        return True
    elif project.dependency_file:
        for l in project.dependency_file.readlines():
            parse_dependencies(l, project)
        return True
    else:
        return False
