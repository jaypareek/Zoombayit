import logging
from django.contrib.auth.models import User
from django.core.validators import validate_email
from rest_framework import viewsets
from rest_framework import status
from .models import *
from .serializers import *
from django.http import JsonResponse
from rest_framework.response import Response
from datetime import datetime
from rest_framework import filters


# logger
logger = logging.getLogger(__name__)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsersList
    


