from __future__ import annotations
from abc import ABC, abstractmethod
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _


class Status(ABC):
    """
    Abstract class for State
    """
    _context = None

    def __init__(self, context: Task):
        """
        take task instance and assign to internal value
        return: None
        """
        self._context = context

    @abstractmethod
    def transmit(self):
        # abstarct method responsed on swith state
        pass


class NewState(Status):
    """
    subclass from state class represent new state
    """
    def transmit(self) -> Status:
        """
        implement abstract method for new state
        return: new state object
        """
        self._context.state = self._context.in_progress
        self._context.save()
        return InProgressState(self._context)

    def update(self, field: str, value: str) -> None:
        """
        add update method only for new state
        return: returned None
        """
        setattr(self._context, field, value)
        self._context.save()


class InProgressState(Status):
    """
    subclass from state class represent In Progress state
    """
    def transmit(self) -> Status:
        """
        implement abstract method for In Progress state
        return: new state object
        """
        self._context.state = self._context.done
        self._context.save()
        return DoneState(self._context)

    def link(self, tasks: list) -> None:
        """
        add link method only for in progress state
        return: returned None
        """
        self._context.hook.add(*tasks)

    def get_link(self):
        """
        add get_link method only for in progress state
        return: Task QuerySet
        """
        hook = self._context.hook.all()
        hook = hook.union(
            self._context.hook_with.all(),
            Task.objects.filter(pk=self._context.pk)
        )
        return hook


class DoneState(Status):
    """
    subclass from state class represent Done state
    """
    def transmit(self) -> None:
        """
        implement abstract method for Done state
        if it call will raise error that we can not dell with this state
        return: raise error that we can't call this method on this state
        """
        raise ValidationError(f'Task {self._context} is in Done State. No change avalible')


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
    hook = models.ManyToManyField('self', related_name='hook_with', symmetrical=False)

    def __init__(self, *args, **kwargs):
        """
        Task constractor we set state class 'status' based on state filed and initiate object
        return: None
        """
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
        """
        map method to map switch to state switch
        return: None
        """
        self.__status = self.__status.transmit()

    def update(self, field: str, value: str) -> Task:
        """
        map method to map update from instance to update from state
        return: new Task instance
        """
        return self.__status.update(field, value)

    def link(self, tasks: list) -> None:
        """
        map link method to state link methos
        """
        self.__status.link(tasks)

    def get_linked_tasks(self):
        """
        amp get linked tasks to statues linked tasks
        """
        return self.__status.get_link()
