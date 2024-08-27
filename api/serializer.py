from rest_framework import serializers
from .models import User
class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model=User
        fields=['email','is_verified']
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class VerifyOtpSerializer(serializers.Serializer):
    email=serializers.EmailField()
    otp=serializers.CharField(max_length=6)
    

        