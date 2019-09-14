from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from django.core.exceptions import ValidationError as DJValidationError
from rest_framework.exceptions import ValidationError, ParseError

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

    @action(detail=True, methods=['patch', ], url_path='update-title')
    def update_title(self, request, pk=None, *args, **kwargs):
        instance = self.get_object()
        try:
            instance.update(field='title', value=request.data.get('title'))
            return super().retrieve(request, *args, **kwargs)
        except AttributeError:
            raise ParseError(f"Task {instance} isn't in New state. You can't change Attribute")

    @action(detail=True, methods=['patch', ], url_path='update-description')
    def update_desc(self, request, pk=None, *args, **kwargs):
        instance = self.get_object()
        try:
            instance.update(field='desc', value=request.data.get('desc'))
            return super().retrieve(request, *args, **kwargs)
        except AttributeError:
            raise ParseError(f"Task {instance} isn't in New state. You can't change Attribute")
