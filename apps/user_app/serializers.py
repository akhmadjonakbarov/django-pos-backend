from rest_framework import serializers

from apps.user_app.models import CustomUserModel


class PublicUserSerializer(serializers.ModelSerializer):
    isAdmin = serializers.SerializerMethodField()

    class Meta:
        model = CustomUserModel
        fields = ('id', 'email', 'token', 'isAdmin', 'first_name', 'last_name', 'address')

    def get_isAdmin(self, user: CustomUserModel):
        return user.is_staff


class RegisterUserSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    password = serializers.CharField(min_length=6, required=True)
    password2 = serializers.CharField(min_length=6, required=True)

    def create(self, validated_data):
        user = CustomUserModel(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class LoginUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUserModel
        fields = ('email', 'password')
