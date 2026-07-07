from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from .utils.response import success_response,error_response
from .serializers import RegisterSerializer, UpdateProfileSerializer, CheckMobileSerializer, GetUserSerializer
from .models import User, Address

# Create your views here.

class UserRegisterAPI(APIView):

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()

            return success_response(
                message="User registered successfully",
                data={
                    "user": serializer.data,
                },
                status=status.HTTP_201_CREATED
            )

        return error_response(
            message="Validation failed",
            errors=serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    

class GetUserAPI(APIView):

    def get(self, request):

        users = User.objects.all()

        serializer = GetUserSerializer(users, many=True)

        return success_response(
            message="Users fetched successfully.",
            data={
                "users": serializer.data
            },
            status=status.HTTP_200_OK
        )
    


class UpdateProfileAPI(APIView):

    def put(self, request, user_id):

        try:
            user = User.objects.get(id=user_id)

        except User.DoesNotExist:
            return error_response(
                message="User not found.",
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = UpdateProfileSerializer(
            user,
            data=request.data
        )

        if serializer.is_valid():

            serializer.save()

            return success_response(
                message="Profile updated successfully.",
                data={
                    "user": serializer.data
                },
                status=status.HTTP_200_OK
            )

        return error_response(
            message="Validation failed.",
            errors=serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    

class CheckMobileAPI(APIView):

    def post(self, request):

        serializer = CheckMobileSerializer(data=request.data)

        if serializer.is_valid():

            mobile_number = serializer.validated_data["mobile_number"]

            exists = User.objects.filter(
                mobile_number=mobile_number
            ).exists()

            return success_response(
                message="Mobile number checked successfully.",
                data={
                    "exists": exists
                },
                status=status.HTTP_200_OK
            )

        return error_response(
            message="Validation failed.",
            errors=serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )