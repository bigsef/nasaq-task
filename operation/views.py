from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from django.core.exceptions import ValidationError as DJValidationError
from rest_framework.exceptions import ValidationError

from .models import Task
from .serializers import TaskSerializer


class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    @action(detail=True, methods=['post'], url_path='change-state')
    def transmit_view(self, request, pk=None, *args, **kwargs):
        instance = self.get_object()
        try:
            instance.transmit()
            return super().retrieve(request, *args, **kwargs)
        except DJValidationError as e:
            raise ValidationError(e.message)