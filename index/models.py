from django.db import models
from django.core.urlresolvers import reverse


class Project(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    description = models.TextField()
    tag = models.ManyToManyField('Tag')

    def get_absolute_url(self):
        return reverse('detail', kwargs={'project_slug': self.slug})

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['-name']


class Repository(models.Model):
    name = models.CharField(max_length=255)
    url = models.URLField()
    project = models.ForeignKey(Project)

    def __unicode__(self):
        return self.name


class Host(models.Model):
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['-name']


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
        return '%s, %s, %s' % (self.project, self.instance_type, self.description)


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
