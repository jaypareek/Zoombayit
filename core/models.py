from django.db import models
from django.contrib.auth.models import User

class Activities(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activity_created_by')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activity_updated_by')

    class Meta:
        verbose_name = "Activity"
        verbose_name_plural = "Activities"

    def __str__(self):
        return self.name

class Classes(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    delivery_date = models.DateField()
    cutoff_date = models.DateField()
    allow_waitlist = models.BooleanField(default=False)
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='instructor')
    activities = models.ManyToManyField(Activities)
    available_slots = models.IntegerField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_by')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='updated_by')

    class Meta:
        verbose_name = "Class"
        verbose_name_plural = "Classes"

    def __str__(self):
        return self.full_name

class Bookings(models.Model):
    client_name = models.CharField(max_length=100)
    client_email = models.EmailField()
    classes = models.ForeignKey(Classes, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='booking_created_by')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='booking_updated_by')
    is_active = models.BooleanField(default=True)
    is_waitlisted = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Booking"
        verbose_name_plural = "Bookings"
        unique_together = (('client_email', 'classes'),)

    def __str__(self):
        return f"{self.user.username} - {self.class_name.name}"
    
