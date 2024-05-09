from django.test import TestCase, Client
from django.urls import reverse
from .models import Vendor, PurchaseOrder, HistoricalPerformance
from .forms import PurchaseOrderForm, VendorForm
from django.utils import timezone
import json

class VendorListViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_vendor_list_view(self):
        url = reverse('vendor_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_vendor_view(self):
        url = reverse('create_vendor')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        # Test POST request with valid data
        data = {'name': 'Test Vendor', 'address': '123 Test St'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)  # Check if it redirects after successful POST


class PurchaseOrderViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.vendor = Vendor.objects.create(name='Test Vendor', address='123 Test St')

    def test_purchase_order_list_view(self):
        url = reverse('purchase_order_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        # Add more assertions as needed

    def test_create_purchase_order_view(self):
        url = reverse('create_purchase_order')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        # Test POST request with valid data
        data = {'po_number': 'PO001', 'vendor': self.vendor.id, 'order_date': timezone.now()}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)  # Check if it redirects after successful POST

    def test_acknowledge_purchase_order_view(self):
        purchase_order = PurchaseOrder.objects.create(po_number='PO001', vendor=self.vendor)
        url = reverse('acknowledge_purchase_order', args=[purchase_order.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)

        # Verify if acknowledgment_date is updated
        updated_po = PurchaseOrder.objects.get(id=purchase_order.id)
        self.assertIsNotNone(updated_po.acknowledgment_date)


class FormTestCase(TestCase):

    def test_invalid_purchase_order_form(self):
        data = {'po_number': '', 'vendor': 1, 'order_date': timezone.now()}
        form = PurchaseOrderForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn('po_number', form.errors)  # Check for specific field error


class ModelTestCase(TestCase):
    def test_vendor_creation(self):
        vendor = Vendor.objects.create(name='Test Vendor', address='123 Test St')
        self.assertIsInstance(vendor, Vendor)
        self.assertEqual(vendor.name, 'Test Vendor')

    def test_purchase_order_creation(self):
        vendor = Vendor.objects.create(name='Test Vendor', address='123 Test St')
        po = PurchaseOrder.objects.create(po_number='PO001', vendor=vendor, order_date=timezone.now())
        self.assertIsInstance(po, PurchaseOrder)
        self.assertEqual(po.po_number, 'PO001')


# Run tests
# python manage.py test vendorProfileManagement
