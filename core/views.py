import logging
from django.contrib.auth.models import User
from django.core.validators import validate_email
from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import action
from .models import *
from .serializers import *
from django.http import JsonResponse
from rest_framework.response import Response
from datetime import datetime
from rest_framework import filters
from rest_framework.exceptions import MethodNotAllowed
from django.core.exceptions import ValidationError
import re

# logger
logger = logging.getLogger(__name__)

# email validation for validating user inputs in booking

def is_valid_email_regex(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

class ClassesViewSet(viewsets.ModelViewSet):
    queryset = Classes.objects.all()
    serializer_class = ClassesSerializer
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
    
    def create(self, request, *args, **kwargs):
        logger.info(f"POST request data: {request.data}")
        
        response = super().create(request, *args, **kwargs)
        
        if response.status_code == status.HTTP_201_CREATED:
            logger.info(f"Created new class: {response.data}")
        else:
            logger.warning(f"Failed to create class: {response.data}")
        
        return response
    
class ActivitiesViewSet(viewsets.ModelViewSet):
    queryset = Activities.objects.all()
    serializer_class = ActivitiesSerializer

    def create(self, request, *args, **kwargs):
        logger.info(f"POST request data: {request.data}")
        
        response = super().create(request, *args, **kwargs)
        
        if response.status_code == status.HTTP_201_CREATED:
            logger.info(f"Created new activity: {response.data}")
        else:
            logger.warning(f"Failed to create activity: {response.data}")
        
        return response
    
class BookingsViewSet(viewsets.ModelViewSet):
    queryset = Bookings.objects.all()
    serializer_class = BookingsSerializer
    http_method_names = ['get']

    def list(self, request, *args, **kwargs):
        email = request.query_params.get('email', None)

        if email:
            try:
                validate_email(email)
                logger.info(f"validated {email}")
            except ValidationError:
                logger.error(f"Invalid email Address {email}")
                return Response(
                    {'error': 'Invalid email address.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            bookings = self.queryset.filter(client_email=email)
            if not bookings.exists():
                return Response(
                    {'error': 'No bookings found for the given email.'},
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            bookings = self.queryset.all()

        serializer = self.get_serializer(bookings, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        raise MethodNotAllowed("POST")

    def update(self, request, *args, **kwargs):
        raise MethodNotAllowed("PUT")

    def partial_update(self, request, *args, **kwargs):
        raise MethodNotAllowed("PATCH")

    def destroy(self, request, *args, **kwargs):
        raise MethodNotAllowed("DELETE")

# as per requirement only post with client email, name and class id 

class BookViewSet(viewsets.ModelViewSet):
    queryset = Classes.objects.all()
    serializer_class = BookSerializer
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        logger.info(f"POST request data: {request.data}")
        
        response = super().create(request, *args, **kwargs)
        
        if response.status_code == status.HTTP_201_CREATED:
            logger.info(f"Created new booking: {response.data}")
        else:
            logger.warning(f"Failed to create booking: {response.data}")
        
        return response
    
    def perform_create(self, serializer):
        user = User.objects.filter(is_superuser=True).first()
        serializer.save(
            created_by=user,
            updated_by=user
        )

    def list(self, request, *args, **kwargs):
        raise MethodNotAllowed("GET")

    def retrieve(self, request, *args, **kwargs):
        raise MethodNotAllowed("GET")

    def update(self, request, *args, **kwargs):
        raise MethodNotAllowed("PUT")

    def partial_update(self, request, *args, **kwargs):
        raise MethodNotAllowed("PATCH")

    def destroy(self, request, *args, **kwargs):
        raise MethodNotAllowed("DELETE")