from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *
from . import views

app_name = 'core'

router = DefaultRouter()
# router.register(r'users', UserViewSet, basename='users')
router.register(r'activities', ActivitiesViewSet, basename='activities')
router.register(r'classes', ClassesViewSet, basename='classes')
router.register(r'bookings', BookingsViewSet, basename='bookings')
router.register(r'book', BookViewSet, basename='book')

urlpatterns = [
#   path('core/', views.my_view, name='mv'),
    path('api/v1.0/', include(router.urls)),
]