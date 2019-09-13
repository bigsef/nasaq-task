from django.db import models
from django.utils.translation import gettext_lazy as _


class Task(models.Model):
    new = 0
    in_progress = 1
    done = 2

    STATE_CHOICE = {
        (new, _('New')),
        (in_progress, _('In Progress')),
        (done, _('Done')),
    }

    title = models.CharField(_('Title'), max_length=50)
    desc = models.TextField(_('Description'))
    state = models.IntegerField(choices=STATE_CHOICE, default=new)

    def __str__(self) -> str:
        """
        Responsible for returning a readable name for the object
        :return string
        """
        return self.title
