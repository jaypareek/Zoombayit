from django.db import models
from django.contrib.auth.models import User

class Activities(models.Model):
    name = models.CharField(max_length=100, unique=True)
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
    delivery_date = models.DateTimeField()
    cutoff_date = models.DateTimeField()
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
        return self.name    

class Bookings(models.Model):
    client_name = models.CharField(max_length=100,default="Micheal Scott")
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

    # reduce slot size of class on each booking on creating the entry and 
    # if class allows waitlist allow saving the row making Waitlist as true and fail if class doesnt allow
    
    def save(self, *args, **kwargs):
        if self.classes.available_slots > 0:
            self.classes.available_slots -= 1
            self.classes.save()
            super().save(*args, **kwargs)
        elif self.classes.allow_waitlist:
            self.is_waitlisted = True
            super().save(*args, **kwargs)
        else:
            raise ValueError("No available slots and class does not allow waitlist")

    def __str__(self):
        return f"{self.client_name} - {self.classes.name}"
    
