from django.contrib import admin
from .models import Accessory, CartItem, Bill, BillItem


# Admin configuration for Accessory model
@admin.register(Accessory)
class AccessoryAdmin(admin.ModelAdmin):
    # Fields to show in list view
    list_display = ['p_name', 'p_cost', 'p_count', 'v_name', 'created_at']

    # Add filters on right side
    list_filter = ['v_name', 'created_at', 'p_cost']

    # Add search functionality
    search_fields = ['p_name', 'p_description', 'v_name']

    # Fields that can't be edited
    readonly_fields = ['created_at', 'updated_at']

    # Fields that can be edited directly in list view
    list_editable = ['p_cost', 'p_count']

    # Default ordering
    ordering = ['-created_at']


# Admin configuration for CartItem model
@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['user', 'accessory', 'quantity', 'total_cost', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'accessory__p_name']
    readonly_fields = ['total_cost', 'created_at']


# Inline admin for BillItem (shows inside Bill admin)
class BillItemInline(admin.TabularInline):
    model = BillItem
    readonly_fields = ['total_cost']
    extra = 0  # Don't show extra empty forms


# Admin configuration for Bill model
@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'total_cost', 'created_at']
    list_filter = ['created_at']
    search_fields = ['customer__username']
    readonly_fields = ['total_cost', 'created_at']
    inlines = [BillItemInline]  # Show bill items inside bill


# Admin configuration for BillItem model
@admin.register(BillItem)
class BillItemAdmin(admin.ModelAdmin):
    list_display = ['bill', 'accessory', 'quantity', 'unit_price', 'total_cost']
    list_filter = ['bill__created_at']
    search_fields = ['accessory__p_name', 'bill__customer__username']
    readonly_fields = ['total_cost']