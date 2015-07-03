import os

from django.db import models
from django.core.urlresolvers import reverse
from django.dispatch import receiver
from django.db.models.signals import post_save
from index.tasks import get_requirements

join = os.path.join


class Project(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    description = models.TextField()
    tag = models.ManyToManyField('Tag')
    dependencies = models.ManyToManyField('Dependency', null=True, blank=True)
    dependency_file = models.FileField(upload_to='dependencies', null=True, blank=True)

    def get_dependencies(self):
        return get_requirements.delay(self)

    @property
    def hosts(self):
        result = []
        for instance in self.instance_set.all():
            try:
                name = instance.host.name
            except:
                continue
            else:
                result.append(name)
        return ', '.join(result)

    def get_absolute_url(self):
        return reverse('detail', kwargs={'project_slug': self.slug})

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Repository(models.Model):
    name = models.CharField(max_length=255)
    url = models.URLField(null=True, blank=True)
    project = models.ForeignKey(Project)

    def __unicode__(self):
        return self.name


class Host(models.Model):
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('hosts:detail', kwargs={'id': self.id})

    def packages(self):
        # get all the packages which should be installed in this host
        dependencies = []
        for instance in self.instance_set.all().select_related():
            for dep in instance.project.dependencies.all():
                if dep not in dependencies:
                    dependencies.append(dep)
        return dependencies

    class Meta:
        ordering = ['name']


class Instance(models.Model):
    instance_type = models.CharField(
        choices=(
            (u'pro', u'Production'),
            (u'stg', u'Staging'),
            (u'dev', u'Development')
        ),
        max_length=3
    )
    url = models.URLField(blank=True)
    path = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    project = models.ForeignKey(Project)
    host = models.ForeignKey(Host, null=True, blank=True)

    def __unicode__(self):
        return '%s, %s, %s' % (
            self.project,
            self.instance_type,
            self.description
        )


class Docs(models.Model):
    name = models.CharField(max_length=255)
    url = models.URLField(max_length=255)
    project = models.ForeignKey(Project)

    def __unicode__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=255)

    def get_absolute_url(self):
        return reverse('tags:detail', kwargs={'name': self.name})

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Dependency(models.Model):
    name = models.CharField(max_length=255)
    package_name = models.SlugField(max_length=255, null=True, blank=True)
    pip_package_name = models.SlugField(max_length=255)
    version = models.CharField(max_length=255, null=True, blank=True)

    @property
    def url(self):
        url = None
        if self.pip_package_name[:3] != 'git':
            url = 'https://pypi.python.org/pypi/%s' % self.pip_package_name
            if self.version:
                url += '/%s' % self.version
        return url or self.pip_package_name.split('git+')[-1]

    def dependent_project_count(self):
        return self.project_set.count()

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']


@receiver(post_save)
def get_dependencies(sender, instance, created, *args, **kwargs):
    if sender == Project:
        instance.get_dependencies()
