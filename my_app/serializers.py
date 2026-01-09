from rest_framework import serializers
from .models import *
# from rest_framework_simplejwt.serializers import TokenObtainPairSerializer



# class UserLoginSerializer(TokenObtainPairSerializer):
#     @classmethod
#     def get_token(cls, user):
#         token = super().get_token(user)
#         return token

class UserOtherInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserOtherInfo
        fields = (
            "first_name",
            "last_name",
            "username",
            "email",
            "password",
        )
        extra_kwargs = {
            "password": {"write_only": True}
        }

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = UserOtherInfo.objects.create_user(
            password=password,
            **validated_data
        )
        return user 



class ProductInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductInfo
        fields = '__all__'        