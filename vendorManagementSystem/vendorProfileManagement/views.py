from django.utils import timezone
import logging
from django.db import IntegrityError
from django.urls import reverse
from rest_framework import generics
from .models import Vendor, PurchaseOrder, HistoricalPerformance
from .serializers import VendorSerializer, PurchaseOrderSerializer, HistoricalPerformanceSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .utils import update_vendor_performance_metrics
from django.shortcuts import render, redirect, get_object_or_404
from .forms import PurchaseOrderForm, VendorForm


class VendorListCreateView(generics.ListCreateAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer


class VendorRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer


class PurchaseOrderListCreateView(generics.ListCreateAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer


class PurchaseOrderRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer


@api_view(['GET', 'POST'])
def acknowledge_purchase_order(request, po_id):
    purchase_order = get_object_or_404(PurchaseOrder, pk=po_id)

    if request.method == 'POST':
        purchase_order.acknowledgment_date = timezone.now()
        purchase_order.save()
        update_vendor_performance_metrics(purchase_order.vendor)
        return redirect('purchase_order_detail', po_id=purchase_order.id)

    context = {'purchase_order': purchase_order}
    return render(request, 'acknowledge_purchase_order.html', context)


@api_view(['GET'])
def vendor_performance(request, vendor_id):
    try:
        vendor = Vendor.objects.get(pk=vendor_id)
    except Vendor.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # Retrieve historical performance records for the vendor
    performance_records = HistoricalPerformance.objects.filter(vendor=vendor)
    try:
        if performance_records.exists():
            # Get the latest performance record for the vendor
            latest_performance = performance_records.latest('date')
            serializer = HistoricalPerformanceSerializer(latest_performance)
            return render(request, 'vendor_performance.html', {'vendor': vendor, 'performance': serializer.data})
        else:
            # No performance records found for the vendor
            return render(request, 'vendor_performance.html', {'vendor': vendor,'performance': None})

    except Exception as e:
        logger.error(f"Error retrieving Purchase Axknowledgement data: {e}")



logger = logging.getLogger(__name__)


def home(request):
    return render(request, 'home.html')


def vendor_list(request):
    vendors = Vendor.objects.all()
    return render(request, 'vendor_list.html', {'vendors': vendors})


def vendor_detail(request, vendor_id):
    try:
        vendor = Vendor.objects.get(id=vendor_id)
    except Exception as e:
        logger.error(f"Error retrieving Vendors: {e}")
        vendor = []
    return render(request, 'vendor_detail.html', {'vendor': vendor})


def create_vendor(request):
    if request.method == 'POST':
        form = VendorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('vendor_list')
    else:
        form = VendorForm()
    return render(request, 'create_vendor.html', {'form': form})


def edit_vendor(request, vendor_id):
    vendor = get_object_or_404(Vendor, id=vendor_id)
    if request.method == 'POST':
        form = VendorForm(request.POST, instance=vendor)
        if form.is_valid():
            form.save()
            return redirect('vendor_detail', vendor_id=vendor_id)
    else:
        form = VendorForm(instance=vendor)
    return render(request, 'edit_vendor.html', {'form': form, 'vendor': vendor})

def delete_vendor(request, vendor_id):
    vendor = get_object_or_404(Vendor, id=vendor_id)

    if request.method == 'POST':
        try:
            vendor.delete()
            return redirect('vendor_list')
        except IntegrityError:
            error_message = "Cannot delete vendor due to related objects (e.g., Purchase Orders)."
            return render(request, 'delete_vendor.html', {'vendor': vendor, 'error_message': error_message})

    return render(request, 'delete_vendor.html', {'vendor': vendor})


def purchase_order_list(request):
    try:
        purchase_orders = PurchaseOrder.objects.all()
    except Exception as e:
        logger.error(f"Error retrieving PurchaseOrders: {e}")
        purchase_orders = []

    return render(request, 'purchase_order_list.html', {'purchase_orders': purchase_orders})


def purchase_order_detail(request, po_id):
    purchase_order = get_object_or_404(PurchaseOrder, id=po_id)
    return render(request, 'purchase_order_detail.html', {'purchase_order': purchase_order})


def create_purchase_order(request):
    if request.method == 'POST':
        form = PurchaseOrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('purchase_order_list')
    else:
        form = PurchaseOrderForm()

    # Render the form template with the form variable (either empty or containing submitted data)
    return render(request, 'create_purchase_order.html', {'form': form})


def edit_purchase_order(request, po_id):
    purchase_order = get_object_or_404(PurchaseOrder, id=po_id)
    if request.method == 'POST':
        form = PurchaseOrderForm(request.POST, instance=purchase_order)
        try:
            if form.is_valid():
                form.save()
                return redirect('purchase_order_detail', po_id=po_id)
        except ValueError as ve:
            form.add_error(None, str(ve))
        except IntegrityError as ie:
            form.add_error(None, str(ie))
    else:
        form = PurchaseOrderForm(instance=purchase_order)
    return render(request, 'edit_purchase_order.html', {'form': form, 'purchase_order': purchase_order})


def delete_purchase_order(request, po_id):
    purchase_order = get_object_or_404(PurchaseOrder, id=po_id)
    if request.method == 'POST':
        purchase_order.delete()
        return redirect('purchase_order_list')
    return render(request, 'delete_purchase_order.html', {'purchase_order': purchase_order})
