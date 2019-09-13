from rest_framework.generics import CreateAPIView

from .models import Task
from .serializers import TaskSerializer


class CreateTaskView(CreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
