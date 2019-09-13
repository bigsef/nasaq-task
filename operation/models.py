from django.db import models
from django.utils.translation import gettext_lazy as _


class Task(models.Model):
    title = models.CharField(_('Title'), max_length=50)
    desc = models.TextField(_('Description'))

    def __str__(self) -> str:
        """
        Responsible for returning a readable name for the object
        :return string
        """
        return self.title
