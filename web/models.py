import datetime

from django.db import models



# from django.db import models
# from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser)
#
#
# class UserManager(BaseUserManager):
#     def create_user(self, email, phone, type, password=None):
#         if not email:
#             raise ValueError('Users must have an email address')
#
#         user = self.model(
#             email=self.normalize_email(email),
#             phone=phone,
#             type=type,
#         )
#
#         user.set_password(password)
#         user.save(using=self._db)
#         return user
#
#     def create_superuser(self, email, phone, password,type):
#         user = self.create_user(
#             email,
#             password=password,
#             phone=phone,
#             type=type,
#         )
#         user.is_admin = True
#         user.save(using=self._db)
#         return user
#
#
# class User(AbstractBaseUser):
#     email = models.EmailField(
#         verbose_name='email',
#         max_length=255,
#         unique=True,
#     )
#     phone = models.DateField()
#     type = models.CharField(max_length=10, default='user')
#     is_active = models.BooleanField(default=True)
#     is_admin = models.BooleanField(default=False)
#
#     objects = UserManager()
#
#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['phone']
#
#     def __str__(self):
#         return self.email
#
#     def has_perm(self, perm, obj=None):
#         return True
#
#     def has_module_perms(self, app_label):
#         return True
#
#     @property
#     def is_staff(self):
#         return self.is_admin
#
#
#










# Create your models here.
class MyUser(models.Model):
    TYPE_CHOICES = (
        ('director', 'Director Sales and Marketing'),
        ('zone', 'Zonal Manager'),
        ('sales', 'Sales Representative'),
    )
    username = models.CharField(max_length=200)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=200)
    password = models.CharField(max_length=100)
    type = models.CharField(max_length=300)
    phone = models.CharField(max_length=100)

    def __str__(self):
        return self.username

class Order(models.Model):
    username = models.CharField(max_length=200)
    product_name = models.CharField(max_length=200)
    quantity = models.CharField(max_length=200)
    rate = models.CharField(max_length=200)
    packing = models.CharField(max_length=200)
    # company = models.CharField(max_length=200)

    def __str__(self):
        return self.username

class zone(models.Model):
    username = models.CharField(max_length=200)
    zone_name = models.CharField(max_length=200)

    def __str__(self):
        return self.zone_name

class dir_connection(models.Model):
    director_name = models.CharField(max_length=200)
    zonal_name = models.CharField(max_length=200)

    def __str__(self):
        return self.director_name

class zone_connection(models.Model):
    zonal_name = models.CharField(max_length=200)
    sales_name = models.CharField(max_length=200)

    def __str__(self):
        return self.zonal_name

class order_sales(models.Model):
    username = models.CharField(max_length=200)
    sales = models.CharField(max_length=200)
    date = models.DateField(default=datetime.date.today)

    def __str__(self):
        return self.sales

class final_order(models.Model):
    username = models.CharField(max_length=200)
    product_name = models.CharField(max_length=200)
    quantity = models.CharField(max_length=200)
    rate = models.CharField(max_length=200)
    date = models.DateField(default=datetime.datetime.now)
    company = models.CharField(max_length=200, default='None')

    def __str__(self):
        return self.username