from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.hashers import make_password
from datetime import date
import re

from .models import User, Address


class RegisterSerializer(serializers.ModelSerializer):

    # Address Fields
    house_no = serializers.CharField(write_only=True)
    state = serializers.CharField(write_only=True)
    pincode = serializers.CharField(write_only=True)

    # Password
    # password = serializers.CharField(
    #     write_only=True,
    #     min_length=6
    # )

    # Optional Email
    email = serializers.EmailField(
        required=False,
        allow_null=True,
        allow_blank=True,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message="Email already exists"
            )
        ]
    )

    # Mobile Number
    mobile_number = serializers.CharField(
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message="Mobile number already exists"
            )
        ]
    )

    class Meta:
        model = User
        fields = [
            "full_name",
            "email",
            "mobile_number",
            "gender",
            "date_of_birth",
            "house_no",
            "state",
            "pincode",
        ]

    # Full Name Validation
    def validate_full_name(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "Full name is required."
            )

        if len(value) < 4:
            raise serializers.ValidationError(
                "Full name must be at least 4 characters."
            )

        return value

    # Email Validation
    def validate_email(self, value):
        if value:
            return value.strip().lower()
        return value

    # Mobile Validation
    def validate_mobile_number(self, value):
        value = value.strip()

        if not re.fullmatch(r'^[6-9]\d{9}$', value):
            raise serializers.ValidationError(
                "Enter a valid 10-digit mobile number."
            )

        return value

    # Gender Validation
    def validate_gender(self, value):
        genders = ["Male", "Female", "Other"]

        if value not in genders:
            raise serializers.ValidationError(
                "Invalid gender."
            )

        return value

    # Date of Birth Validation
    def validate_date_of_birth(self, value):
        if value >= date.today():
            raise serializers.ValidationError(
                "Date of birth cannot be today or a future date."
            )

        return value
    
    def validate_house_no(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "House number is required."
            )

        if len(value) < 2:
            raise serializers.ValidationError(
                "House number must be at least 2 characters."
            )

        return value
    
    # State Validation
    def validate_state(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "State is required."
            )

        if len(value) < 2:
            raise serializers.ValidationError(
                "State name is too short."
            )

        return value
    

    def validate_pincode(self, value):
        value = value.strip()

        if not re.fullmatch(r'^\d{6}$', value):
            raise serializers.ValidationError(
                "Enter a valid 6-digit pincode."
            )

        return value



    # Password Validation
    # def validate_password(self, value):

    #     if len(value) < 6:
    #         raise serializers.ValidationError(
    #             "Password must be at least 6 characters."
    #         )

    #     return value

    # Create User & Address
    def create(self, validated_data):

        house_no = validated_data.pop("house_no")
        state = validated_data.pop("state")
        pincode = validated_data.pop("pincode")

        # validated_data["password"] = make_password(
        #     validated_data["password"]
        # )

        user = User.objects.create(**validated_data)

        Address.objects.create(
            user=user,
            house_no=house_no,
            state=state,
            pincode=pincode
        )

        return user
    

from rest_framework import serializers
from .models import User


class GetUserSerializer(serializers.ModelSerializer):

    house_no = serializers.CharField(source="address.house_no", read_only=True)
    state = serializers.CharField(source="address.state", read_only=True)
    pincode = serializers.CharField(source="address.pincode", read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "full_name",
            "email",
            "mobile_number",
            "gender",
            "date_of_birth",
            "house_no",
            "state",
            "pincode",
            "created_at",
        ]


class UpdateProfileSerializer(serializers.ModelSerializer):

    house_no = serializers.CharField(write_only=True)
    state = serializers.CharField(write_only=True)
    pincode = serializers.CharField(write_only=True)

    email = serializers.EmailField(
        required=False,
        allow_blank=True,
        allow_null=True
    )

    class Meta:
        model = User
        fields = [
            "full_name",
            "email",
            "mobile_number",
            "gender",
            "date_of_birth",
            "house_no",
            "state",
            "pincode",
        ]

    # Full Name Validation
    def validate_full_name(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "Full name is required."
            )

        if len(value) < 4:
            raise serializers.ValidationError(
                "Full name must be at least 4 characters."
            )

        return value

    # Email Validation (Optional)
    def validate_email(self, value):

        if value in [None, ""]:
            return value

        value = value.strip().lower()

        if User.objects.exclude(id=self.instance.id).filter(email=value).exists():
            raise serializers.ValidationError(
                "Email already exists."
            )

        return value

    # Mobile Validation
    def validate_mobile_number(self, value):

        value = value.strip()

        if not re.fullmatch(r'^[6-9]\d{9}$', value):
            raise serializers.ValidationError(
                "Enter a valid 10-digit mobile number."
            )

        if User.objects.exclude(id=self.instance.id).filter(
            mobile_number=value
        ).exists():
            raise serializers.ValidationError(
                "Mobile number already exists."
            )

        return value

    # Gender Validation
    def validate_gender(self, value):

        if value not in ["Male", "Female", "Other"]:
            raise serializers.ValidationError(
                "Invalid gender."
            )

        return value

    # Date of Birth Validation
    def validate_date_of_birth(self, value):

        if value >= date.today():
            raise serializers.ValidationError(
                "Date of birth cannot be today or a future date."
            )

        return value

    # House Number Validation
    def validate_house_no(self, value):

        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "House number is required."
            )

        return value

    # State Validation
    def validate_state(self, value):

        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "State is required."
            )

        return value

    # Pincode Validation
    def validate_pincode(self, value):

        value = value.strip()

        if not re.fullmatch(r'^\d{6}$', value):
            raise serializers.ValidationError(
                "Enter a valid 6-digit pincode."
            )

        return value

    # Update User & Address
    def update(self, instance, validated_data):

        house_no = validated_data.pop("house_no", None)
        state = validated_data.pop("state", None)
        pincode = validated_data.pop("pincode", None)

        instance.full_name = validated_data.get(
            "full_name",
            instance.full_name
        )

        instance.email = validated_data.get(
            "email",
            instance.email
        )

        instance.mobile_number = validated_data.get(
            "mobile_number",
            instance.mobile_number
        )

        instance.gender = validated_data.get(
            "gender",
            instance.gender
        )

        instance.date_of_birth = validated_data.get(
            "date_of_birth",
            instance.date_of_birth
        )

        instance.save()

        address, created = Address.objects.get_or_create(user=instance)

        if house_no is not None:
            address.house_no = house_no

        if state is not None:
            address.state = state

        if pincode is not None:
            address.pincode = pincode

        address.save()

        return instance
    



class CheckMobileSerializer(serializers.Serializer):

    mobile_number = serializers.CharField()

    def validate_mobile_number(self, value):
        value = value.strip()

        if not re.fullmatch(r'^[6-9]\d{9}$', value):
            raise serializers.ValidationError(
                "Enter a valid 10-digit mobile number."
            )

        return value
    
