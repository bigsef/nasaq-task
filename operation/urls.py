from rest_framework.routers import DefaultRouter

from .views import TaskViewSet

app_name = 'operation'

# Task ViewSet router
route = DefaultRouter()
route.register('', TaskViewSet)
urlpatterns = route.urls
