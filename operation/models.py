from __future__ import annotations
from abc import ABC, abstractmethod
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _


class Status(ABC):
    _context = None

    def __init__(self, context: Task):
        self._context = context

    @abstractmethod
    def transmit(self):
        pass


class NewState(Status):
    def transmit(self) -> Status:
        self._context.state = self._context.in_progress
        self._context.save()
        return InProgressState(self._context)


class InProgressState(Status):
    def transmit(self) -> Status:
        self._context.state = self._context.done
        self._context.save()
        return DoneState(self._context)


class DoneState(Status):
    def transmit(self) -> None:
        raise ValidationError('Task is in Done State. No change avalible')


class Task(models.Model):
    new = 0
    in_progress = 1
    done = 2

    STATE_CHOICE = {
        (new, _('New')),
        (in_progress, _('InProgress')),
        (done, _('Done')),
    }

    title = models.CharField(_('Title'), max_length=50)
    desc = models.TextField(_('Description'))
    state = models.IntegerField(_('State'), choices=STATE_CHOICE, default=new)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        StateClass = eval(f'{self.get_state_display()}State')
        self.__status = StateClass(self)

    def __str__(self) -> str:
        """
        Responsible for returning a readable name for the object
        :return string
        """
        return f'{self.title} have ID:{self.pk}'

    def transmit(self) -> None:
        self.__status = self.__status.transmit()

    def update(self, field: str, value: str) -> Task:
        return self.__status.update(field, value)

    def link(self, task: Task) -> None:
        self.__status.link(task)

    def get_linked_tasks(self, task_id: int):
        return self.__status.get_link(task_id)
