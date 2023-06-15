from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db.models import OneToOneField
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

# Create your models here.

"""The manager class does NOT have any field names, rather it has two methods. 
One method is used to create regular users, the other method is used to create superusers"""


class UserManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, email, password=None):

        if not email:
            raise ValueError('User must have email address')

        if not username:
            raise ValueError('User must have an username')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name
        )
        user.set_password(password)  # coding password
        user.save(using=self._db)
        return user

    # the function works when admin account is created
    def create_superuser(self, first_name, last_name, username, email, password=None):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)


class User(AbstractBaseUser):
    VENDOR = 1
    CUSTOMER = 2
    ROLE_CHOICE = (
        (VENDOR, 'Restaurant'),
        (CUSTOMER, 'Customer')
    )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=12, blank=True)  # regrex
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICE, blank=True, null=True)

    # required fields
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    create_date = models.DateTimeField(auto_now_add=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)  # not to verify account, because if its not active you cant login
    is_superadmin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = UserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    def get_role(self):
        if self.role == 1:
            user_role = 'Vendor'
        else:
            user_role = 'Customer'
        return user_role


# when you create user it should also be created
class UserProfile(models.Model):
    """
    OneToOneField, meaning that each instance of the model containing this field
    will have a one-to-one relationship with an instance of the Django built-in User model

    CASCADE option is specified, which means that when a User instance is deleted,
    all instances of the model containing this OneToOneField will also be deleted.

    The "blank=True" argument indicates that the field is allowed to be left blank when creating an instance of the model
    """
    user = OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)  # taki foreign key do tabeli user
    profile_picture = models.ImageField(upload_to='users/profile_pictures', blank=True, null=True)
    cover_photo = models.ImageField(upload_to='users/cover_photos', blank=True, null=True)
    address_line_1 = models.CharField(max_length=50, blank=True, null=True)
    address_line_2 = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=15, blank=True, null=True)
    state = models.CharField(max_length=15, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    pin_code = models.CharField(max_length=6, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)  # date is unchangeable
    modified_at = models.DateTimeField(auto_now=True)  # when object is modyfied date will be changed

    def __str__(self):
        return self.user.email


@receiver(post_save, sender=User)
def post_save_create_profile_receiver(sender, instance, created, **kwargs):
    # print(created)
    if created:
        UserProfile.objects.create(user=instance)
        print('create the user profile')
    else:
        try:
            profile = UserProfile.objects.get(user=instance)
            profile.save()
        except:
            UserProfile.objects.create(user=instance)
            print('Profile was not exist, but I created one')
        print('user is updated')


# 26 - signal episode
@receiver(pre_save, sender=User)
def pre_save_profile_receiver(sender, instance, **kwargs):
    print(instance.username, 'this user is being saved')
