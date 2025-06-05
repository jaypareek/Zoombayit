from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from datetime import datetime, timedelta
from django.utils import timezone
import pytz

from .models import Activities, Classes, Bookings
from .serializers import ActivitiesSerializer, ClassesSerializer, BookingsSerializer

class ModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        
        self.activity = Activities.objects.create(
            name='Test Activity',
            description='Test Description',
            created_by=self.user,
            updated_by=self.user
        )
        
        self.class_obj = Classes.objects.create(
            name='Test Class',
            description='Test Class Description',
            delivery_date=timezone.now() + timedelta(days=7),
            cutoff_date=timezone.now() + timedelta(days=5),
            allow_waitlist=True,
            instructor=self.user,
            available_slots=10,
            created_by=self.user,
            updated_by=self.user
        )
        self.class_obj.activities.add(self.activity)
        
    def test_activity_creation(self):
        self.assertEqual(self.activity.name, 'Test Activity')
        self.assertEqual(str(self.activity), 'Test Activity')
        
    def test_class_creation(self):
        self.assertEqual(self.class_obj.name, 'Test Class')
        self.assertEqual(self.class_obj.available_slots, 10)
        self.assertEqual(str(self.class_obj), 'Test Class')
        
    def test_booking_creation(self):
        booking = Bookings.objects.create(
            client_name='Test Client',
            client_email='client@example.com',
            classes=self.class_obj,
            created_by=self.user,
            updated_by=self.user
        )
        self.assertEqual(booking.client_name, 'Test Client')
        self.assertEqual(booking.is_waitlisted, False)
        self.assertEqual(self.class_obj.available_slots, 9)
        self.assertEqual(str(booking), 'Test Client - Test Class')
        
    def test_booking_waitlist(self):
        # Create a class with no available slots
        no_slot_class = Classes.objects.create(
            name='Full Class',
            description='Full Class Description',
            delivery_date=timezone.now() + timedelta(days=7),
            cutoff_date=timezone.now() + timedelta(days=5),
            allow_waitlist=True,
            instructor=self.user,
            available_slots=0,
            created_by=self.user,
            updated_by=self.user
        )
        
        booking = Bookings.objects.create(
            client_name='Waitlist Client',
            client_email='waitlist@example.com',
            classes=no_slot_class,
            created_by=self.user,
            updated_by=self.user
        )
        
        self.assertEqual(booking.is_waitlisted, True)
        
    def test_booking_no_slots_no_waitlist(self):
        # Create a class with no available slots and no waitlist
        no_slot_class = Classes.objects.create(
            name='Full Class No Waitlist',
            description='Full Class Description',
            delivery_date=timezone.now() + timedelta(days=7),
            cutoff_date=timezone.now() + timedelta(days=5),
            allow_waitlist=False,
            instructor=self.user,
            available_slots=0,
            created_by=self.user,
            updated_by=self.user
        )
        
        with self.assertRaises(ValueError):
            Bookings.objects.create(
                client_name='Rejected Client',
                client_email='rejected@example.com',
                classes=no_slot_class,
                created_by=self.user,
                updated_by=self.user
            )


class APITestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        # Create a regular user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        
        # Create a superuser for BookViewSet
        self.superuser = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpassword'
        )
        
        self.activity = Activities.objects.create(
            name='Test Activity',
            description='Test Description',
            created_by=self.user,
            updated_by=self.user
        )
        
        self.class_obj = Classes.objects.create(
            name='Test Class',
            description='Test Class Description',
            delivery_date=timezone.now() + timedelta(days=7),
            cutoff_date=timezone.now() + timedelta(days=5),
            allow_waitlist=True,
            instructor=self.user,
            available_slots=10,
            created_by=self.user,
            updated_by=self.user
        )
        self.class_obj.activities.add(self.activity)
        
        self.booking = Bookings.objects.create(
            client_name='Test Client',
            client_email='client@example.com',
            classes=self.class_obj,
            created_by=self.user,
            updated_by=self.user
        )
        
        # URLs
        self.activities_url = reverse('core:activities-list')
        self.classes_url = reverse('core:classes-list')
        self.bookings_url = reverse('core:bookings-list')
        self.book_url = reverse('core:book-list')
        
    def test_get_activities(self):
        response = self.client.get(self.activities_url)
        activities = Activities.objects.all()
        serializer = ActivitiesSerializer(activities, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
        
    def test_create_activity(self):
        data = {
            'name': 'New Activity',
            'description': 'New Description',
            'created_by': self.user.id,
            'updated_by': self.user.id
        }
        response = self.client.post(self.activities_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Activities.objects.count(), 2)
        
    def test_get_classes(self):
        response = self.client.get(self.classes_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        
    def test_get_bookings(self):
        response = self.client.get(self.bookings_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        
    def test_get_bookings_by_email(self):
        url = f"{self.bookings_url}?email=client@example.com"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        
    def test_get_bookings_by_invalid_email(self):
        url = f"{self.bookings_url}?email=invalid"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_get_bookings_by_nonexistent_email(self):
        url = f"{self.bookings_url}?email=nonexistent@example.com"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
    # Modified test_create_booking to handle the NOT NULL constraint issue
    def test_create_booking(self):
        # The BookViewSet.perform_create method uses User.objects.filter(is_superuser=True).first()
        # So we need to make sure a superuser exists before making the request
        
        data = {
            'client_name': 'New Client',
            'client_email': 'new@example.com',
            'classes': self.class_obj.id
        }
        
        # Make sure we have a superuser in the database
        if not User.objects.filter(is_superuser=True).exists():
            User.objects.create_superuser(
                username='admin2',
                email='admin2@example.com',
                password='adminpassword'
            )
            
        response = self.client.post(self.book_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Check if available slots decreased
        self.class_obj.refresh_from_db()
        self.assertEqual(self.class_obj.available_slots, 8)  # Started with 10, -1 in setUp, -1 now
        
    def test_booking_methods_not_allowed(self):
        # Test that BookingsViewSet only allows GET
        response = self.client.post(self.bookings_url, {})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        
        response = self.client.put(f"{self.bookings_url}{self.booking.id}/", {})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        
        response = self.client.patch(f"{self.bookings_url}{self.booking.id}/", {})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        
        response = self.client.delete(f"{self.bookings_url}{self.booking.id}/")
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        
    def test_book_methods_not_allowed(self):
        # Test that BookViewSet only allows POST
        response = self.client.get(self.book_url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        
        response = self.client.put(f"{self.book_url}1/", {})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        
        response = self.client.patch(f"{self.book_url}1/", {})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        
        response = self.client.delete(f"{self.book_url}1/")
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)