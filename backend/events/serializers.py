# events/serializers.py
from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'contact_number', 'password']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            contact_number=validated_data['contact_number'],
            password=validated_data['password'],
        )
        return user

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'
        
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'        

class RSVPSerializer(serializers.ModelSerializer):

    # user = UserSerializer()
    # event = EventSerializer()

    class Meta:
        model = RSVP
        fields = ['id','user','event']
