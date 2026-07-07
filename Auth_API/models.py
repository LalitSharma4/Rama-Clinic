from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager



class User(AbstractBaseUser, PermissionsMixin):

    GENDER_CHOICES = (
        ("Male", "Male"),
        ("Female", "Female"),
        ("Other", "Other"),
    )

    full_name = models.CharField(max_length=150)

    mobile_number = models.CharField(
        max_length=10,
        unique=True
    )

    email = models.EmailField(
        unique=True,
        blank=True,
        null=True
    )

    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES
    )

    date_of_birth = models.DateField()


    is_active = models.BooleanField(default=True)

    is_staff = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = "mobile_number"

    REQUIRED_FIELDS = []

    def __str__(self):
        return self.full_name
    
    class Meta:
        db_table = "USER"


class Address(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="address"
    )

    house_no = models.CharField(max_length=255)


    state = models.CharField(max_length=100)

    pincode = models.CharField(max_length=6)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.full_name} Address"
    
    class Meta:
        db_table = "ADDRESS"