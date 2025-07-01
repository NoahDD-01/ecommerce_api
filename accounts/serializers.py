from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenBlacklistSerializer
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import Group, Permission
from .models import User
from accounts.helpers import mmt # Myanmar time formatter
from django.utils import timezone

class CustomTokenObtainPairSerializer(serializers.Serializer):
    login = serializers.CharField()
    password = serializers.CharField(style={"input_type":"password"})

    def validate(self, attrs):
        login = attrs.get("login")
        password = attrs.get("password")

        user = authenticate(
            request=self.context.get("request"),
            username = login,
            password=password,
        )
        if not user:
            raise AuthenticationFailed(
                _("Invalid username/email/phone or password"), code="authorization"
            )
        if not user.is_active:
            raise AuthenticationFailed(_("Account is disabled."), code="authorization")
        
        user.last_login = timezone.now()
        user.save(update_fields=['last_login'])
        user.refresh_from_db(fields=["last_login"])

        refresh = RefreshToken.for_user(user)
        return{
            "refresh":str(refresh),
            "access": str(refresh.access_token),
            "user":{
                "id": user.id,
                "username" : user.uername,
                "email": user.email,
                "phone": user.phone,
                "date_joined": mmt(user.date_joined),
                "last_login" : mmt(user.last_login),
                
                },
                "message":"Login Successful",
        }
    
