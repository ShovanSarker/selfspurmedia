from django.db import models
from subscriber.models import Subscriber
# Create your models here.


class Package(models.Model):
    name = models.CharField(max_length=64)
    remarks = models.TextField(blank=True, null=True)
    limit = models.IntegerField(default=0)
    isActive = models.BooleanField(default=True)
    dateAdded = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __unicode__(self):
        return self.name


class SubscribedPackage(models.Model):
    subscriber = models.ForeignKey(Subscriber, related_name='WhoSubscribedThisPackage')
    numberOfPost = models.IntegerField(default=0)
    package = models.ForeignKey(Package, related_name='WhichPacked')
    dateAdded = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __unicode__(self):
        return self.subscriber.name


class PackageRequest(models.Model):
    subscriber = models.ForeignKey(Subscriber, related_name='WhoWantsToSubscribeThisPackage')
    package = models.ForeignKey(Package, related_name='WhichPackedDoTheyNeed')
    isPending = models.BooleanField(default=True)
    status = models.CharField(max_length=16, null=True, blank=True)
    dateAdded = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __unicode__(self):
        return self.subscriber.name
