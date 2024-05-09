from django.urls import path, include
from django.contrib import admin
from vendorProfileManagement import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),

    ##################### VENDORS ###############################################################
    path('api/vendors/', views.vendor_list, name='vendor_list'),
    path('api/vendors/<int:vendor_id>/', views.vendor_detail, name='vendor_detail'),
    path('api/vendors/create/', views.create_vendor, name='create_vendor'),
    path('api/vendors/edit/<int:vendor_id>', views.edit_vendor, name='edit_vendor'),
    path('api/vendors/delete/<int:vendor_id>', views.delete_vendor, name='delete_vendor'),
    path('api/vendors/<int:vendor_id>/performance/', views.vendor_performance, name='vendor_performance'),

    ############### Purchase Order UI ###########################################################
    path('purchase_orders/', views.purchase_order_list, name='purchase_order_list'),
    path('purchase_orders/<int:po_id>/', views.purchase_order_detail, name='purchase_order_detail'),
    path('purchase_orders/create/', views.create_purchase_order, name='create_purchase_order'),
    path('purchase_orders/<int:po_id>/edit/', views.edit_purchase_order, name='edit_purchase_order'),
    path('purchase_orders/<int:po_id>/delete/', views.delete_purchase_order, name='delete_purchase_order'),
    path('purchase_orders/<int:po_id>/acknowledge/', views.acknowledge_purchase_order,
         name='acknowledge_purchase_order'),
]
