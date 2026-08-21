import datetime

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models


ROLE_CHOICES = (
    (0, 'visitor'),
    (1, 'librarian'),
)


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifier
    for authentication instead of usernames.
    """

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError('The Email must be set')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('role', 1)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must have is_staff=True.'
            )

        if extra_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must have is_superuser=True.'
            )

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    This class represents a basic user.
    """

    first_name = models.CharField(
        max_length=20,
        default=''
    )

    last_name = models.CharField(
        max_length=20,
        default=''
    )

    middle_name = models.CharField(
        max_length=20,
        default=''
    )

    email = models.CharField(
        max_length=100,
        unique=True,
        default=None
    )

    password = models.CharField(
        default=None,
        max_length=255
    )

    created_at = models.DateTimeField(
        editable=False,
        auto_now=datetime.datetime.now()
    )

    updated_at = models.DateTimeField(
        auto_now=datetime.datetime.now()
    )

    role = models.IntegerField(
        choices=ROLE_CHOICES,
        default=0
    )

    is_active = models.BooleanField(default=False)

    is_staff = models.BooleanField(default=False)

    id = models.AutoField(primary_key=True)

    USERNAME_FIELD = 'email'

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def __repr__(self):
        return f"{CustomUser.__name__}(id={self.id})"

    @staticmethod
    def get_by_id(user_id):
        """
        Return user by ID or None.
        """
        custom_user = CustomUser.objects.filter(id=user_id).first()
        return custom_user if custom_user else None

    @staticmethod
    def get_by_email(email):
        """
        Return user by email or None.
        """
        custom_user = CustomUser.objects.filter(email=email).first()
        return custom_user if custom_user else None

    @staticmethod
    def delete_by_id(user_id):
        """
        Delete user by ID.
        """
        user_to_delete = CustomUser.objects.filter(id=user_id).first()

        if user_to_delete:
            CustomUser.objects.filter(id=user_id).delete()
            return True

        return False

    @staticmethod
    def create(
        email,
        password,
        first_name=None,
        middle_name=None,
        last_name=None
    ):
        """
        Create a new user and save it to the database.
        """
        if (
            len(first_name) <= 20
            and len(middle_name) <= 20
            and len(last_name) <= 20
            and len(email) <= 100
            and len(email.split('@')) == 2
            and len(CustomUser.objects.filter(email=email)) == 0
        ):
            custom_user = CustomUser(
                email=email,
                password=password,
                first_name=first_name,
                middle_name=middle_name,
                last_name=last_name
            )

            custom_user.save()
            return custom_user

        return None

    def to_dict(self):
        """
        Return user data as a dictionary.
        """
        return {
            'id': self.id,
            'first_name': f'{self.first_name}',
            'middle_name': f'{self.middle_name}',
            'last_name': f'{self.last_name}',
            'email': f'{self.email}',
            'created_at': int(self.created_at.timestamp()),
            'updated_at': int(self.updated_at.timestamp()),
            'role': self.role,
            'is_active': self.is_active
        }

    def update(
        self,
        first_name=None,
        last_name=None,
        middle_name=None,
        password=None,
        role=None,
        is_active=None
    ):
        """
        Update user profile in the database.
        """
        user_to_update = CustomUser.objects.filter(
            email=self.email
        ).first()

        if first_name is not None and len(first_name) <= 20:
            user_to_update.first_name = first_name

        if last_name is not None and len(last_name) <= 20:
            user_to_update.last_name = last_name

        if middle_name is not None and len(middle_name) <= 20:
            user_to_update.middle_name = middle_name

        if password is not None:
            user_to_update.password = password

        if role is not None:
            user_to_update.role = role

        if is_active is not None:
            user_to_update.is_active = is_active

        user_to_update.save()

    @staticmethod
    def get_all():
        """
        Return all users.
        """
        return CustomUser.objects.all()

    def get_role_name(self):
        """
        Return role name.
        """
        return ROLE_CHOICES[self.role][1]