from django.db import models
from subscriber.models import Subscriber
from product.models import Product

# Create your models here.


class Review(models.Model):
    subscriber = models.ForeignKey(Subscriber, related_name='WhoReviewedThisProduct')
    product = models.ForeignKey(Product, related_name='WhichProductWasRated')
    rating = models.IntegerField(default=0)
    review = models.TextField(blank=True, null=True)
    dateAdded = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __unicode__(self):
        return self.product.name
