from django.db import models
from product.models import Category

# Create your models here.


class Subscriber(models.Model):
    name = models.CharField(max_length=128)
    email = models.EmailField(null=True, blank=True)
    secretQuestion = models.CharField(max_length=128)
    secretAnswer = models.CharField(max_length=128)
    isAdmin = models.BooleanField(default=False)
    isProductOwner = models.BooleanField(default=False)
    isActive = models.BooleanField(default=True)
    numberOfReviews = models.IntegerField(default=0, null=True, blank=True)
    dateAdded = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __unicode__(self):
        return self.name


class Settings(models.Model):
    logoImage = models.FileField("LogoImage", upload_to="settingsImages", blank=True, null=True)
    bannerImage1 = models.FileField("BannerImage1", upload_to="settingsImages", blank=True, null=True)
    bannerImage2 = models.FileField("BannerImage2", upload_to="settingsImages", blank=True, null=True)
    bannerImage3 = models.FileField("BannerImage3", upload_to="settingsImages", blank=True, null=True)
    advertise1 = models.FileField("AdvImage1", upload_to="settingsImages", blank=True, null=True)
    advertise2 = models.FileField("AdvImage2", upload_to="settingsImages", blank=True, null=True)
    scroller1 = models.ForeignKey(Category, related_name="categoryForScroller1", null=True, blank=True)
    scroller2 = models.ForeignKey(Category, related_name="categoryForScroller2", null=True, blank=True)
    scroller3 = models.ForeignKey(Category, related_name="categoryForScroller3", null=True, blank=True)
    address = models.CharField(max_length=74, blank=True, null=True)
    callCenterNumber = models.CharField(max_length=20, blank=True, null=True)
    howItWorksStep1Image = models.FileField("HowStep1Image", upload_to="settingsImages", blank=True, null=True)
    howItWorksStep1Title = models.CharField(max_length=24, blank=True, null=True)
    howItWorksStep1Description = models.TextField(blank=True, null=True)
    howItWorksStep2Image = models.FileField("HowStep2Image", upload_to="settingsImages", blank=True, null=True)
    howItWorksStep2Title = models.CharField(max_length=24, blank=True, null=True)
    howItWorksStep2Description = models.TextField(blank=True, null=True)
    howItWorksStep3Image = models.FileField("HowStep3Image", upload_to="settingsImages", blank=True, null=True)
    howItWorksStep3Title = models.CharField(max_length=24, blank=True, null=True)
    howItWorksStep3Description = models.TextField(blank=True, null=True)
    howItWorksStep4Image = models.FileField("HowStep4Image", upload_to="settingsImages", blank=True, null=True)
    howItWorksStep4Title = models.CharField(max_length=24, blank=True, null=True)
    howItWorksStep4Description = models.TextField(blank=True, null=True)
    facebookURL = models.CharField(max_length=50, null=True, blank=True)
    twitterURL = models.CharField(max_length=50, null=True, blank=True)
    youtubeURL = models.CharField(max_length=50, null=True, blank=True)
    linkedinURL = models.CharField(max_length=50, null=True, blank=True)
    aboutUS = models.TextField(null=True, blank=True)
    termsAndCondition = models.TextField(null=True, blank=True)
    dateAdded = models.DateTimeField(auto_now=True, auto_now_add=True)

    def __unicode__(self):
        return self.dateAdded