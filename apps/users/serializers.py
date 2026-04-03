from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from apps.users.models import User

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, min_length=8, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True, min_length=8, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2', 'role', 'phone_number', 'address')
        extra_kwargs = {'role': {'required': False}}

    def validate_role(self, value):
        if value == User.Role.ADMIN:
            raise serializers.ValidationError("You cannot register as admin.")
        return value

    def validate_email(self, value):
        # if email already exists
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists")
        return value

    def validate_username(self, value):
        # if username already exists
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists")
        return value

    def validate(self, data):
        # if pw do not match
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Passwords don't match")
        return data

    def create(self, validated_data):
        # remove password2 before create user
        validated_data.pop('password2')
        password = validated_data.pop('password')

        user = User(**validated_data)
        user.set_password(password) # hash pw
        user.save()
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        # authenticate check email and pw
        user = authenticate(username=email, password=password)

        if not user:
            raise serializers.ValidationError("Invalid email or password")
        if not user.is_active:
            raise serializers.ValidationError("This account is not active")

        # generate JWT token
        refresh = RefreshToken.for_user(user)

        return {
            'user': user,
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        }

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'role', 'phone_number', 'address', 'created_at')
        read_only_fields = ('id', 'email', 'role', 'created_at')