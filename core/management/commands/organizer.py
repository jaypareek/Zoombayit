import logging
import csv
import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.core.management import call_command
from core.models import *
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime



# logger
logger = logging.getLogger(__name__)

def create_super_user():
    User = get_user_model()
    if not User.objects.filter(is_superuser=True).exists():
        try:
            User.objects.create_superuser(username='admin', email='admin@zoo.com', password='admin')
            logger.info('Superuser created successfully using organizer')
        except Exception as e:
            logger.error(f'Error creating superuser: {e}')
        return True
    else:
        return False
def create_activities():
    # this function will create activities required for classes to be created fetching activities data from csv file

    csv_file_path = 'file/organizer/activities.csv'

    if not os.path.exists(csv_file_path):
        error_msg = f"CSV file does not exist: {csv_file_path}"
        logger.error(error_msg)
        return

    try:
        with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            created_count = 0

            for row_number, row in enumerate(reader, start=2):
                try:
                    activity = Activities.objects.create(
                        name=row['name'],
                        description=row['description'],
                        created_by=User.objects.filter(is_superuser=True).first(),
                        updated_by=User.objects.filter(is_superuser=True).first()
                    )
                    created_count += 1
                    logger.info(f"Created Activity: {activity.name}")
                except Exception as e:
                    logger.error(f"Row {row_number} in {csv_file_path}: Failed to create activity Error: {e}")
                
            logger.info(f"Import finished. Total activities created: {created_count}")

    except Exception as e:
        logger.exception(f"Unexpected error during CSV import of in {csv_file_path}: {e}")


def create_classes():
    # this function will create activities required for classes to be created fetching activities data from csv file

    csv_file_path = 'file/organizer/classes.csv'

    if not os.path.exists(csv_file_path):
        error_msg = f"CSV file does not exist: {csv_file_path}"
        logger.error(error_msg)
        return

    try:
        with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            created_count = 0

            for row_number, row in enumerate(reader, start=2):
                try:
                    naive_delivery_dt = datetime.strptime(row['delivery_date'], '%Y-%m-%d %H:%M:%S')
                    naive_cutoff_dt = datetime.strptime(row['cutoff_date'], '%Y-%m-%d %H:%M:%S')
                    delivery_dt = timezone.make_aware(naive_delivery_dt)
                    cutoff_dt = timezone.make_aware(naive_cutoff_dt)
                    classes = Classes.objects.create(
                        name=row['name'],
                        description=row['description'],
                        delivery_date=delivery_dt,
                        cutoff_date=cutoff_dt,
                        allow_waitlist=bool(row['allow_waitlist']),
                        instructor=User.objects.get(id=row['instructor']),
                        available_slots=row['available_slots'],
                        created_by=User.objects.filter(is_superuser=True).first(),
                        updated_by=User.objects.filter(is_superuser=True).first()
                    )
                    activity_ids = [int(pk.strip()) for pk in row['activities'].split(',')]
                    activities = Activities.objects.filter(id__in=activity_ids)
                    classes.activities.set(activities)
                    created_count += 1
                    logger.info(f"Created Class: {classes.name}")
                except Exception as e:
                    logger.error(f"Row {row_number} in {csv_file_path}: Failed to create class Error: {e}")
                
            logger.info(f"Import finished. Total classes created: {created_count}")

    except Exception as e:
        logger.exception(f"Unexpected error during CSV import of in {csv_file_path}: {e}")

def create_bookings():
    # this function will create activities required for classes to be created fetching activities data from csv file

    csv_file_path = 'file/organizer/bookings.csv'

    if not os.path.exists(csv_file_path):
        error_msg = f"CSV file does not exist: {csv_file_path}"
        logger.error(error_msg)
        return

    try:
        with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            created_count = 0

            for row_number, row in enumerate(reader, start=2):
                try:
                    booking = Bookings.objects.create(
                        client_name=row['name'],
                        client_email=row['email'],
                        classes=Classes.objects.get(id=row['class']),
                        created_by=User.objects.filter(is_superuser=True).first(),
                        updated_by=User.objects.filter(is_superuser=True).first()
                    )
                    created_count += 1
                    logger.info(f"Created Booking for: {booking.client_name}")
                except Exception as e:
                    logger.error(f"Row {row_number} in {csv_file_path}: Failed to create booking Error: {e}")
                
            logger.info(f"Import finished. Total bookings created: {created_count}")

    except Exception as e:
        logger.exception(f"Unexpected error during CSV import of in {csv_file_path}: {e}")

class Command(BaseCommand):
    help = 'creates a superuser activities, classes, and sample bookins'

    def handle(self, *args, **options):
        user_created = create_super_user()
        
        if user_created:
            self.stdout.write(self.style.SUCCESS('Superuser created successfully : Login "admin" and "admin" '))
            try:
                create_activities()
                create_classes()
                create_bookings()
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error creating activities, classes, and bookings: {e}'))

        else:
            self.stdout.write(self.style.SUCCESS('Superuser already exists!'))
            try:
                create_activities()
                create_classes()
                create_bookings()
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error creating activities, classes, and bookings: {e}'))
                
        self.stdout.write(self.style.SUCCESS('Successfully executed Organizer'))