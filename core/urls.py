from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *
from . import views

app_name = 'core'

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')


urlpatterns = [
#   path('core/', views.my_view, name='mv'),
    path('api/v1.0/', include(router.urls)),
]