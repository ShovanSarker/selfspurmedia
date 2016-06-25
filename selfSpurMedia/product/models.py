from django.db import models
from subscriber.models import Subscriber
# Create your models here.


class Type(models.Model):
    name = models.CharField(max_length=64)
    remarks = models.TextField(blank=True, null=True)
    image = models.FileField("Category Image", upload_to="categoryImages", blank=True, null=True)
    isActive = models.BooleanField(default=True)
    dateAdded = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __unicode__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=64)
    remarks = models.TextField(blank=True, null=True)
    image = models.FileField("Category Image", upload_to="categoryImages", blank=True, null=True)
    isActive = models.BooleanField(default=True)
    isPendingForApproval = models.BooleanField(default=True)
    dateAdded = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __unicode__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=64)
    remarks = models.TextField(blank=True, null=True)
    image = models.FileField("Brand Image", upload_to="brandImages", blank=True, null=True)
    isActive = models.BooleanField(default=True)
    isPendingForApproval = models.BooleanField(default=True)
    dateAdded = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __unicode__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=64)
    image1 = models.FileField("ProductImage1", upload_to="productImages", blank=True, null=True)
    image2 = models.FileField("ProductImage2", upload_to="productImages", blank=True, null=True)
    image3 = models.FileField("ProductImage3", upload_to="productImages", blank=True, null=True)
    image4 = models.FileField("ProductImage4", upload_to="productImages", blank=True, null=True)
    image5 = models.FileField("ProductImage5", upload_to="productImages", blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    type = models.ForeignKey(Type, related_name='ProductType')
    category = models.ForeignKey(Category, related_name='ProductCategory')
    brand = models.ForeignKey(Brand, related_name='ProductBrand')
    addedBy = models.ForeignKey(Subscriber, related_name='ProductAddedBy')
    totalNumberOfRating = models.IntegerField(default=0)
    totalNumberOfStars = models.IntegerField(default=0)
    isActive = models.BooleanField(default=True)
    isPendingForApproval = models.BooleanField(default=True)
    dateAdded = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __unicode__(self):
        return self.name
