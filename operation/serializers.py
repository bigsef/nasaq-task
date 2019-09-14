from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    state = serializers.ChoiceField(
        choices=Task.STATE_CHOICE,
        source='get_state_display',
        read_only=True
    )

    class Meta:
        model = Task
        exclude = 'hook',

    def update(self, instance, validated_data):
        raise ValidationError(f'Not allowed to edit {instance.title} after creation')
