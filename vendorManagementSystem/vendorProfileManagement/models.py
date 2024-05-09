
from django.db import models
import json

from django.utils import timezone


class Vendor(models.Model):
    name = models.CharField(max_length=255)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(max_length=50, unique=True)
    on_time_delivery_rate = models.FloatField(default=0.0)
    quality_rating_avg = models.FloatField(default=0.0)
    average_response_time = models.FloatField(default=0.0)
    fulfillment_rate = models.FloatField(default=0.0)

    def __str__(self):
        return self.name

class PurchaseOrder(models.Model):
    po_number = models.CharField(max_length=50, unique=True)
    vendor = models.ForeignKey(Vendor, related_name='purchase_orders', on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    delivery_date = models.DateTimeField(default=timezone.now, blank=True)
    items = models.TextField()
    # items = models.JSONField(default=list)
    quantity = models.IntegerField(default=0)
    status = models.CharField(max_length=20, default='pending')  # Choices: pending, completed, canceled
    quality_rating = models.FloatField(null=True, blank=True)
    issue_date = models.DateTimeField(auto_now_add=True)
    acknowledgment_date = models.DateTimeField(default=timezone.now, blank=True)

    def __str__(self):
        return self.po_number

    # def save(self, *args, **kwargs):
    #     # Validate and serialize items to JSON format before saving
    #     print("type of items", type(self.items))
    #     if not isinstance(self.items, list):
    #         # If items is not a list, handle or raise an error as needed
    #         raise ValueError("Items must be provided as a list")
    #
    #     # Serialize items to JSON format
    #     self.items = json.dumps(self.items)
    #     print("self.items after json dump", self.items)
    #
    #     super().save(*args, **kwargs)

class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateTimeField()
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()

    def __str__(self):
        return f"{self.vendor.name} - {self.date}"
