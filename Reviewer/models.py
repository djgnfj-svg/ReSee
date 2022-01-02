import string
import random
from typing import Sized

from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class TimeStampedModel(models.Model):
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

class PayPlan(TimeStampedModel):
    name = models.CharField(max_length=20)
    price = models.IntegerField()

class Organization(TimeStampedModel):
    name = models.CharField(max_length=50)
    pay_plan = models.ForeignKey(PayPlan, on_delete=models.DO_NOTHING, null=True)

class Users(AbstractUser):
    email = models.EmailField(max_length=100, null=True, unique=True)
    organization = models.ForeignKey(Organization, on_delete=models.DO_NOTHING, null=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

class Categories(TimeStampedModel):
    category_name = models.CharField(max_length=100)
    organization = models.ForeignKey(Organization, on_delete=models.DO_NOTHING, null=True)
    created_by = models.ForeignKey(Users, on_delete=models.CASCADE)

class StudyList(TimeStampedModel):
    def rand_string():
        str_pool = string.digits + string.ascii_letters
        return ("".join([random.choice(str_pool) for _ in range(6)])).lower()

    def rand_letter():
        str_pool = string.ascii_letters
        return random.choice(str_pool).lower()

    review_count = models.IntegerField(null=False)
    category_id = models.ForeignKey(Categories, on_delete=models.CASCADE, null=True)
    created_by = models.ForeignKey(Users, on_delete=models.CASCADE)    
    study_topic = models.CharField(max_length=30)
    study_contect = models.TextField()

    def review_count_up(self):
        self.review_count += 1
        self.save()
