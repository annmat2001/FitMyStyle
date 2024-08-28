from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.contrib.auth import get_user_model

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, verbose_name="Email Address")
    first_name = models.CharField(max_length=30, verbose_name="First Name")
    last_name = models.CharField(max_length=30, verbose_name="Last Name")
    phone_number = models.CharField(max_length=15, blank=True, verbose_name="Phone Number")
    city = models.CharField(max_length=100, blank=True, verbose_name="City")
    pincode = models.CharField(max_length=10, blank=True, verbose_name="Pincode")
    address = models.TextField(blank=True, verbose_name="Address")
    birth_date = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    def get_short_name(self):
        return self.first_name    
    def get_profile_picture_url(self):
        if self.profile_picture and hasattr(self.profile_picture, 'url'):
            return self.profile_picture.url
        return None  # or return a default image URL
    @property
    def orders_count(self):
        # Placeholder for future implementation
        return 0
    @property
    def reviews_count(self):
        # Placeholder for future implementation
        return 0

User = get_user_model()

class CustomerMeasurements(models.Model):
    customer = models.OneToOneField(User, on_delete=models.CASCADE)
    height = models.FloatField(null=True, blank=True)
    torso = models.FloatField(null=True, blank=True)
    chest = models.FloatField(null=True, blank=True)
    waist = models.FloatField(null=True, blank=True)
    neck = models.FloatField(null=True, blank=True)
    sleeve = models.FloatField(null=True, blank=True)
    inseam = models.FloatField(null=True, blank=True)
    hip = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Measurements for {self.customer.email}"   

