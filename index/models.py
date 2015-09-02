import os

from django.db import models
from django.core.urlresolvers import reverse
from django.dispatch import receiver
from django.db.models.signals import post_save
from index.tasks import get_requirements, get_readme

join = os.path.join


class Project(models.Model):
    name = models.CharField("Project", max_length=255)
    slug = models.SlugField(max_length=255)
    related_project = models.ForeignKey('self', null=True, blank=True)

    description = models.TextField(
        help_text=u'Auto generated if blank and repo is public',
        null=True,
        blank=True
    )
    tag = models.ManyToManyField('Tag')
    dependencies = models.ManyToManyField('Dependency', null=True, blank=True)
    dependency_file = models.FileField(
        upload_to='dependencies',
        null=True,
        blank=True
    )
    public = models.BooleanField(default=True)

    def get_dependencies(self):
        return get_requirements.delay(self)

    def get_readme(self):
        return get_readme.delay(self)

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

    @property
    def databases(self):
        result = []
        for instance in self.instance_set.all():
            dbs = instance.databases
            if dbs:
                result.append(dbs)
        return ', '.join(result)

    def get_absolute_url(self):
        return reverse('detail', kwargs={'project_slug': self.slug})

    def get_wiki_url(self):
        return reverse('wiki:project_detail', kwargs={'project_slug': self.slug})

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Repository(models.Model):
    name = models.CharField(max_length=255)
    url = models.URLField(null=True, blank=True)
    project = models.ForeignKey(Project)
    public = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name


class Host(models.Model):
    name = models.CharField(max_length=255)

    @property
    def cronjob_list(self):
        result = []
        for cronjob in self.cronjob_set.all():
            result.append(cronjob.name)
        return ', '.join(result)

    @property
    def project_list(self):
        result = []
        for project in self.instance_set.all().select_related():
            result.append('%s (%s)' % (project.project.name, project.instance_type))
        return ', '.join(result)

    def __unicode__(self):
        return self.name

    def get_wiki_url(self):
        return reverse('wiki:host_detail', kwargs={'host_id': self.id})

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


class Virtualenv(models.Model):
    name = models.CharField(max_length=255)
    path = models.CharField(max_length=255, default='Please enter a valid virtualenv path')

    def __unicode__(self):
        return self.name


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
    virtualenv = models.ForeignKey(Virtualenv, null=True, blank=True)

    @property
    def databases(self):
        result = []
        for db in self.database_set.all():
            try:
                name = db.name
            except:
                continue
            else:
                result.append(name)
        return ', '.join(result)

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


class Cronjob(models.Model):
    name = models.CharField(max_length=255)
    project = models.ForeignKey(Project, null=True, blank=True)
    command = models.CharField(max_length=255)
    hosts = models.ManyToManyField(Host)
    period = models.CharField(max_length=255)
    user = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(null=True, blank=True)

    def get_absolute_url(self):
        return reverse('cronjobs:detail', kwargs={'id': self.id})

    def get_wiki_url(self):
        return reverse('wiki:cronjob_detail', kwargs={'cronjob_id': self.id})

    def __unicode__(self):
        return self.name

    @property
    def cron_command(self):
        return '%s %s %s' % (self.period, self.user or '', self.command)

    @property
    def host_list(self):
        result = []
        for host in self.hosts.all():
            result.append(host.name)
        return ', '.join(result)


class Database(models.Model):
    name = models.CharField(max_length=255)
    user = models.CharField(max_length=255, blank=True)
    passwd = models.CharField("Password", max_length=255, blank=True)
    host = models.CharField(max_length=255, blank=True)
    port = models.CharField(max_length=255, default='default')
    engine = models.CharField(max_length=255, default='mysql')
    app_name = models.CharField(max_length=255, blank=True)
    instance = models.ForeignKey(Instance)

    def get_absolute_url(self):
        return reverse('databases:detail', kwargs={'id': self.id})

    def get_wiki_url(self):
        return reverse('wiki:database_detail', kwargs={'database_id': self.id})

    def __unicode__(self):
        return self.name


@receiver(post_save)
def get_dependencies(sender, instance, created, *args, **kwargs):
    if sender == Project:
        instance.get_dependencies()
        if not instance.description:
            instance.get_readme()
    if sender == Dependency:
        if not instance.package_name:
            pack_name = instance.pip_package_name.lower()
            if not pack_name.startswith('python-'):
                pack_name = 'python-' + pack_name
            instance.package_name = pack_name
            instance.save()
