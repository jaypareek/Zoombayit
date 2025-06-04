from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *
from . import views

# router = DefaultRouter()
# router.register(r'classes', , basename='classess')

app_name = 'core'

urlpatterns = [
#   path('core/', views.my_view, name='mv'),
]