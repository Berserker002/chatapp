from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.contrib.auth import authenticate

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    age = serializers.IntegerField()
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    interests = serializers.JSONField()

    class Meta:
        model = User
        fields = ['name', 'age', 'password', 'interests', 'is_online']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            name=validated_data['name'],
            age=validated_data['age'],
            password=validated_data['password'],
            interests=validated_data['interests'],
        )
        return user

class UserLoginSerializer(serializers.Serializer):
    name = serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'})

    def validate(self, data):
        name = data.get('name')
        password = data.get('password')

        user = authenticate(username=name, password=password)

        if not user:
            raise serializers.ValidationError('Invalid credentials')

        data['user'] = user
        return data
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'interests', 'is_online']

class UserRecommendation(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'interests', 'is_online']