from django.forms import ValidationError
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from NidsModels.models.auth import Profile
from django.contrib.auth.models import User
from NidsSerializer.auth import (
    RegisterSerializer,
    LoginSerializer,
    ProfileUpdateSerializer,
    ProfileSerializer,
)
from NidsUtilites.auth import ModelAPIView
from django.contrib.auth.password_validation import (
    validate_password,
    password_validators_help_texts,
)
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import traceback


@swagger_auto_schema(
    method="post",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "username": openapi.Schema(
                type=openapi.TYPE_STRING, description="user name"
            ),
            "password": openapi.Schema(
                type=openapi.TYPE_STRING, description="password"
            ),
            "email": openapi.Schema(
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_EMAIL,
                description="email id",
            ),
            "role": openapi.Schema(type=openapi.TYPE_STRING, description="role"),
        },
        required=[
            "username",
            "password",
            "email",
            "role",
        ],
    ),
    responses={
        status.HTTP_200_OK: "Registered successfully",
        status.HTTP_400_BAD_REQUEST: "Bad Request",
        status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal Server Error",
    },
    operation_summary="Register a new user",
    operation_description="""Help to register a new user. role choices are ['Network Admin', 'Security Analyst', 'Guest']""",
)
@api_view(
    [
        "POST",
    ]
)
def register(request):
    """
    view for user registration
    """

    try:

        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():

            username = serializer.validated_data["username"]
            password = serializer.validated_data["password"]
            email = serializer.validated_data["email"]
            role = serializer.validated_data["role"]
            try:
                validate_password(password)
            except ValidationError as ex:
                constr = password_validators_help_texts()
                return Response(
                    status=400,
                    data={"msg": "Try a Difficult Password", "Constrain": constr},
                )

            if len(User.objects.filter(username=username)) > 0:
                return Response(status=400, data={"msg": "Username already in use."})

            if len(User.objects.filter(email=email)) > 0:
                return Response(status=400, data={"msg": "Email already in use."})

            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
            )

            if len(Profile.objects.filter(user=user)) == 0:
                Profile.objects.create(user=user, role=role)

            return Response(status=200, data={"msg": "registeration successful"})

        else:
            return Response(status=400, data=serializer.errors)

    except Exception as ex:
        if str(ex).endswith("already exists"):
            return Response(status=200, data={"msg": "User created successfully"})

        tb = traceback.format_exc()
        return Response(status=500, data={"msg": tb})


@swagger_auto_schema(
    method="post",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "username": openapi.Schema(
                type=openapi.TYPE_STRING, description="user name"
            ),
            "password": openapi.Schema(
                type=openapi.TYPE_STRING, description="password"
            ),
        },
        required=[
            "username",
            "password",
        ],
    ),
    responses={
        status.HTTP_200_OK: "Login successfully",
        status.HTTP_400_BAD_REQUEST: "Bad Request",
        status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal Server Error",
    },
    operation_summary="Login existing user",
    operation_description="""Help to login a existing user.""",
)
@api_view(["POST", "OPTIONS"])
def login(request):
    """
    view for login
    """

    try:

        serializer = LoginSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():

            user = serializer.validated_data
            print(user)
            if not user.is_active:
                return Response(status=401, data={"msg": "unauthorised action"})

            refresh_token = RefreshToken.for_user(user)

            response_data = {
                "tokens": {
                    "refresh_token": str(refresh_token),
                    "access_token": str(refresh_token.access_token),
                },
                "user": {
                    "username": user.username,
                    "email": user.email,
                },
            }
            return Response(status=200, data=response_data)

        else:
            return Response(
                status=400, data={"msg": str(serializer.errors)}
            )

    except Exception as ex:
        tb = traceback.format_exc()
        return Response(status=500, data={"msg": f"Internal server error. Error: {tb}"})


@swagger_auto_schema(
    method="post",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "first_name": openapi.Schema(
                type=openapi.TYPE_STRING, description="first_name"
            ),
            "last_name": openapi.Schema(
                type=openapi.TYPE_STRING, description="last_name"
            ),
            "designation": openapi.Schema(
                type=openapi.TYPE_STRING, description="designation"
            ),
            "date_of_birth": openapi.Schema(
                type=openapi.TYPE_STRING, description="date_of_birth"
            ),
            "gender": openapi.Schema(type=openapi.TYPE_STRING, description="gender"),
            "address": openapi.Schema(type=openapi.TYPE_STRING, description="address"),
            "role": openapi.Schema(type=openapi.TYPE_STRING, description="role"),
        },
        required=[
            "first_name",
            "last_name",
            "designation",
            "date_of_birth",
            "gender",
            "address",
            "role",
        ],
    ),
    responses={
        status.HTTP_200_OK: "update profile successfully",
        status.HTTP_400_BAD_REQUEST: "Bad Request",
        status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal Server Error",
    },
    operation_summary="Update user profile",
    operation_description="""Help to update user profile.""",
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def update_profile(request):
    """
    view to update profile
    """
    try:

        user = request.user
        serializer = ProfileUpdateSerializer(data=request.data)

        if serializer.is_valid():

            args = [
                "first_name",
                "last_name",
                "designation",
                "date_of_birth",
                "gender",
                "address",
                "role",
            ]

            for arg in args:
                setattr(user.profile, arg, serializer.validated_data.get(arg))

            user.profile.save()
            return Response(status=200, data={"msg": "profile updated sucessfully"})

        else:
            return Response(status=400)

    except Exception as ex:
        print("Internal Server Error -> ", str(ex))
        return Response(status=500, data={"msg": "Internal Server Error"})


@swagger_auto_schema(
    method="get",
    manual_parameters=[],
    responses={
        status.HTTP_200_OK: "Profile rendered successfully",
        status.HTTP_400_BAD_REQUEST: "Bad Request",
        status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal Server Error",
    },
    operation_summary="get profile information",
    operation_description="""get user profile details.
    Response: {
        'first_name': "",
        'last_name': "",
        'designation': "",
        'date_of_birth': "",
        'gender': "",
        'address': "",
        'role': ""
    }
    """,
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_profile(request):
    """
    view to get profile
    """
    try:
        serializer = ProfileSerializer(request.user.profile)
        return Response(status=200, data=serializer.data)

    except Exception as ex:
        print("Internal Server Error -> ", str(ex))
        return Response(status=500, data={"msg": "Internal Server Error"})


class UserExists(ModelAPIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "userName",
                openapi.IN_QUERY,
                description="User Name",
                type=openapi.TYPE_STRING,
            ),
        ],
        responses={200: "OK", 400: "No data found."},
        operation_summary="User existance",
        operation_description="""API for user existance.
        """,
    )
    def get(self, request):
        """
        Handle GET request for retrieving details of existance of user.

        Args:
            request: The HTTP request object.

        Returns:
            Response: The HTTP response containing details of existance of user.
        """
        user_name = request.GET.get("userName")

        if User.objects.filter(username=user_name).exists:
            exist_flag = True
        else:
            exist_flag = False

        return Response(data={"isUser": exist_flag}, status=200)
