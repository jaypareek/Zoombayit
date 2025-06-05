import pytz
from rest_framework import serializers
from .models import *
from django.utils import timezone

# all the model's serializers are created.

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class ClassesSerializer(serializers.ModelSerializer):
    
    delivery_date_local = serializers.SerializerMethodField()
    cutoff_date_local = serializers.SerializerMethodField()
    server_timezone = serializers.SerializerMethodField()
    server_time = serializers.SerializerMethodField()

    class Meta:
        model = Classes
        fields = '__all__'  
        read_only_fields = ('server_timezone', 'server_time','delivery_date_local', 'cutoff_date_local')

    def get_timezone(self):
        request = self.context.get('request')
        tzname = request.query_params.get('tz') if request else None
        try:
            return pytz.timezone(tzname) if tzname else timezone.get_current_timezone()
        except pytz.UnknownTimeZoneError:
            return timezone.get_current_timezone()

    def convert_to_user_timezone(self, dt):
        if not dt:
            return None
        user_tz = self.get_timezone()
        if timezone.is_naive(dt):
            dt = timezone.make_aware(dt)
        return dt.astimezone(user_tz).isoformat()

    def get_delivery_date_local(self, obj):
        return self.convert_to_user_timezone(obj.delivery_date)

    def get_cutoff_date_local(self, obj):
        return self.convert_to_user_timezone(obj.cutoff_date)
    
    def get_server_timezone(self, obj):
        return str(timezone.get_current_timezone())

    def get_server_time(self, obj):
        return timezone.now().isoformat()

class ActivitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Activities
        fields = '__all__'

class BookingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookings
        fields = '__all__'

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookings
        fields = '__all__'
        read_only_fields = ('is_active','is_waitlisted','created_by', 'updated_by')

    def validate(self, data):
        classes = data['classes']

        if classes.available_slots <= 0 and not classes.allow_waitlist:
            raise serializers.ValidationError("No available slots and class does not allow waitlist")
        return data
    
    # preventing over booking and waitlisting if allowed
    def create(self, validated_data):
        classes = validated_data['classes']
        if classes.available_slots > 0:
            classes.available_slots -= 1
            classes.save()
            validated_data['is_waitlisted'] = False
        else:
            validated_data['is_waitlisted'] = True 
        return super().create(validated_data)