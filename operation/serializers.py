from rest_framework import serializers

from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    state = serializers.ChoiceField(
        choices=Task.STATE_CHOICE,
        source='get_state_display',
        read_only=True
    )

    class Meta:
        model = Task
        fields = '__all__'
