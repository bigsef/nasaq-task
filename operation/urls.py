from django.urls import path

from .views import CreateTaskView

app_name = 'operation'


urlpatterns = [
    path('add/', CreateTaskView.as_view(), name='create'),
]
