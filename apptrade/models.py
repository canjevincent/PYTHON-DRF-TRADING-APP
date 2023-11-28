from django.db import models
from django.utils import timezone
from django.conf import settings

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.

class Market(models.Model):
  id = models.AutoField(primary_key=True)
  stock_name = models.CharField(max_length=200, blank=False, null=False, unique=True)
  stock_price = models.FloatField(default=0.00, blank=False, null=False)
  stock_quantity = models.IntegerField(default=0, blank=False, null=False)
  created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name="user_market_item")
  created_at = models.DateTimeField(default=timezone.now)

class Order(models.Model):
  id = models.AutoField(primary_key=True)
  quantity_order = models.IntegerField(default=1, blank=False, null=False)
  total_price_order = models.FloatField(default=0.00, blank=False, null=False)
  market_order = models.ForeignKey(Market, on_delete=models.DO_NOTHING)
  created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name="user_market_order")
  ordered_at = models.DateTimeField(default=timezone.now)

class CustomAccountManager(BaseUserManager):

  def create_superuser(self, user_name, password, **other_fields):

    return self.create_user(user_name, password, **other_fields)
  
  def create_user(self, user_name, password, **other_fields):

    if not user_name:
      raise ValueError("username is required.")
    
    if not password:
      raise ValueError("password is required.")
    
    user = self.model(user_name=user_name, **other_fields)
    user.set_password(password)
    user.save()
    return user

class CustomUser(AbstractBaseUser):
  id = models.AutoField(primary_key=True)
  user_name = models.CharField(max_length=150, unique=True)
  date_created = models.DateTimeField(default=timezone.now)
  objects = CustomAccountManager()

  USERNAME_FIELD = "user_name"