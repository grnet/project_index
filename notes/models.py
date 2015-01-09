from django.db import models
from django.core.urlresolvers import reverse

from index.models import Tag


class Note(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    tag = models.ManyToManyField(Tag)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('notes:detail', kwargs={'id': self.pk})

