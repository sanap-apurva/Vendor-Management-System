from django.db.models import Count, F, Avg
from django.db.models.functions import Coalesce
from .models import Vendor, PurchaseOrder


def update_vendor_performance_metrics(vendor):
    completed_pos = vendor.purchase_orders.filter(status='completed')

    # Calculate on-time delivery rate
    on_time_deliveries = completed_pos.filter(delivery_date__lte=F('acknowledgment_date')).count()
    total_completed_pos = completed_pos.count()
    vendor.on_time_delivery_rate = on_time_deliveries / total_completed_pos if total_completed_pos else 0.0

    # Calculate quality rating average
    quality_rating_avg = completed_pos.filter(quality_rating__isnull=False).aggregate(avg_quality_rating=Avg('quality_rating'))
    vendor.quality_rating_avg = quality_rating_avg['avg_quality_rating'] or 0.0

    # Calculate average response time
    response_time_avg = completed_pos.filter(acknowledgment_date__isnull=False).annotate(
        response_time=F('acknowledgment_date') - F('issue_date')
    ).aggregate(avg_response_time=Avg('response_time'))
    vendor.average_response_time = response_time_avg['avg_response_time'].total_seconds() if response_time_avg['avg_response_time'] else 0.0

    # Calculate fulfillment rate
    total_purchase_orders = vendor.purchase_orders.count()
    total_completed_purchase_orders = completed_pos.count()
    vendor.fulfillment_rate = total_completed_purchase_orders / total_purchase_orders if total_purchase_orders > 0 else 0.0

    vendor.save()
