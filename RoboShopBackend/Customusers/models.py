from django.db import models
from django.contrib.auth.models import AbstractUser, Permission, Group, BaseUserManager
# Create your models here.

class UserManager(BaseUserManager):
    use_in_migrations = True
    
    def create(self, email, password = None, **extra_field):
        if not email:
            raise ValueError("Email is Required!")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_field)
        user.set_password(password)
        user.save(using = self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault('is_active',True)
        extra_fields.setdefault('is_staff',True)
        return self.create(email=email,password=password,**extra_fields)

#Custome User registration
class Users(AbstractUser):
    username = None
    email = models.EmailField(
        verbose_name='Email',
        max_length=255,
        unique=True,
    )
    first_name = models.CharField(max_length=500,null=True,blank=True)
    last_name = models.CharField(max_length=500,null=True,blank=True)
    is_active = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    balance = models.IntegerField(default=0)
    phone = models.CharField(max_length=15, blank=True, null=True)
    balance_ref = models.CharField(max_length=500,null=True,blank=True)
    address = models.CharField(max_length=1000,null=True,blank=True)
    password_forget_token = models.CharField(max_length=300,null=True,blank=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name']
    
    groups = models.ManyToManyField(Group, related_name='custom_user_set', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_set', blank=True)
    
    objects = UserManager()
    