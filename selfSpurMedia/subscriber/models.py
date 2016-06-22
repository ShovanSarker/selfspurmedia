from django.db import models

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
