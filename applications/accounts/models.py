from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.db import models


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The given username must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.create_activation_code()
        user.save(using=self._db)
        return user

    def create_user(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


EXPERIENCE = (
    ('personally, privately', 'personally, privately'),
    ('personally, professionally', 'personally, professionally'),
    ('online', 'online'),
    ('other', 'other')
)

AUDIENCE = (
    ('not at the moment', 'not at the moment'),
    ('I have a small audience', 'I have a small audience'),
    ('I have a sufficient audience', 'I have a sufficient audience')
)


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    first_name = models.CharField(max_length=55)
    last_name = models.CharField(max_length=55)
    experience = models.CharField(max_length=55, choices=EXPERIENCE)
    audience = models.CharField(max_length=55, choices=AUDIENCE)
    is_active = models.BooleanField(default=False)
    is_mentor = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    activation_code = models.CharField(max_length=100, blank=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def create_activation_code(self):
        import uuid
        code = str(uuid.uuid4())
        self.activation_code = code







