from django.db import models
from index.models import Tag


class Note(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    tag = models.ManyToManyField(Tag)

    def __unicode__(self):
        return self.title
