from django.contrib.auth import authenticate
from rest_framework import serializers
from NidsModels.models.auth import Profile
from django.contrib.auth.models import User
from axes.models import AccessAttempt


class RegisterSerializer(serializers.Serializer):
    """
    Serializer for register data
    """

    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()
    role = serializers.CharField()

    def validate_role(self, data):
        ROLES = ["Network Admin", "Security Analyst", "Guest"]
        if data not in ROLES:
            raise serializers.ValidationError("{} Role is not Valid".format(data))
        return data


class LoginSerializer(serializers.ModelSerializer):
    """
    Serializer for Login Data
    """

    username = serializers.CharField()
    password = serializers.CharField()

    class Meta:
        model = User
        fields = ["username", "password"]

    def validate(self, data):
        req = self.context["request"]
        user = authenticate(**data, request=req)
        if user:
            return user
        else:
            x = AccessAttempt.objects.filter(username=data["username"])
            no_of_failure = 0
            for i in x:
                no_of_failure += i.failures_since_start
            if no_of_failure < 4:
                raise serializers.ValidationError("Invalid Credentials")
            else:
                raise serializers.ValidationError("User Blocked")


class ProfileUpdateSerializer(serializers.Serializer):
    """
    Serializer for update_profile data
    """

    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    designation = serializers.CharField(required=False)
    date_of_birth = serializers.DateField(required=False)
    gender = serializers.CharField(required=False)
    address = serializers.CharField(required=False)
    role = serializers.CharField(required=False)


class ProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for Profile model
    """

    class Meta:
        model = Profile
        fields = [
            "first_name",
            "last_name",
            "designation",
            "date_of_birth",
            "gender",
            "address",
            "role",
        ]
