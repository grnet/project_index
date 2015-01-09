from django.db import models
from django.core.urlresolvers import reverse


class Meeting(models.Model):
    date = models.DateTimeField()
    description = models.TextField()
    outcome = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return '%s' % self.date

    def get_absolute_url(self):
        return reverse('meetings:detail', kwargs={'id': self.pk})
