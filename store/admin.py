from django.contrib import admin

# Import all models
from .models import (
    Store,
    Product,
    Order,
    OrderItem,
    Review
)


# ============================================================
# Store Admin
# ============================================================

@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):

    # Display these columns in the admin
    list_display = (
        "name",
        "owner",
    )

    # Allow searching by store name and owner
    search_fields = (
        "name",
        "owner__username",
    )


# ============================================================
# Product Admin
# ============================================================

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    # Display product information
    list_display = (
        "name",
        "store",
        "price",
        "stock",
    )

    # Filter by store
    list_filter = (
        "store",
    )

    # Allow searching
    search_fields = (
        "name",
    )


# ============================================================
# Order Admin
# ============================================================

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    # Display order information
    list_display = (
        "id",
        "customer",
        "total",
        "created_at",
    )

    # Allow searching by customer username
    search_fields = (
        "customer__username",
    )


# ============================================================
# Order Item Admin
# ============================================================

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):

    # Display order item information
    list_display = (
        "order",
        "product",
        "quantity",
        "price",
    )


# ============================================================
# Review Admin
# ============================================================

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):

    # Display review information
    list_display = (
        "product",
        "user",
        "rating",
        "verified_purchase",
        "created_at",
    )

    # Add filters
    list_filter = (
        "rating",
        "verified_purchase",
    )

    # Allow searching
    search_fields = (
        "product__name",
        "user__username",
    )