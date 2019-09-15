from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    """
    Serializer Class responsed on how to handel Task representation
    """
    # state field map state model field and not allowed to edit
    state = serializers.ChoiceField(
        choices=Task.STATE_CHOICE,
        source='get_state_display',
        read_only=True
    )

    class Meta:
        model = Task
        # exclude hook relation to mange from state class
        exclude = 'hook',

    def update(self, instance, validated_data):
        """
        override update method to not allow edit Task object and transfer handling to State class
        """
        raise ValidationError(f'Not allowed to edit {instance.title} after creation')
