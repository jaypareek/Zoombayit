from django.db import models
from django.contrib.auth.models import User

class Activities(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activity_created_by')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activity_updated_by')

    def __str__(self):
        return self.name

class Classes(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    delivery_date = models.DateField()
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='instructor')
    activities = models.ManyToManyField(Activities)
    available_slots = models.IntegerField()
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_by')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='updated_by')

    def __str__(self):
        return self.full_name
