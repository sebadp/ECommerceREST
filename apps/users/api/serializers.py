from rest_framework import serializers
from apps.users.models import User
from django.core.exceptions import ValidationError

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class TestUserSerializer(serializers.Serializer):
    name= serializers.CharField(max_length=200)
    email= serializers.EmailField()

    def validate_name(self, value):
        # custom validation
        if 'develop' in value:
            raise serializers.ValidationError('Error, ese nombre está banneado.')

        return value

    def validate_email(self, value):
        
        # validation:empty email
        if value == "":
            raise serializers.ValidationError("Error, este campo no está completado.")
        
        return value

    def validate(self, data):
        print(data)
        return data


    def create(self, validated_data):
        print(validated_data)
        return User.objects.create(**validated_data)