from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.products, name='products'),
    path('stores/', views.stores, name='stores'),
    path('about/', views.about, name='about'),

    path('register/', views.register, name='register'),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout_view"),

    path("vendor/", views.vendor_dashboard, name="vendor_dashboard"),
    path("create-store/", views.create_store, name="create_store"),
    path("create-product/", views.create_product, name="create_product"),
    path(
        "edit-store/<int:store_id>/",
        views.edit_store,
        name="edit_store"
    ),
    path(
        "delete-store/<int:store_id>/",
        views.delete_store,
        name="delete_store"
    ),
    path(
        "edit-product/<int:product_id>/",
        views.edit_product,
        name="edit_product"
    ),
    path(
        "delete-product/<int:product_id>/",
        views.delete_product,
        name="delete_product"
    ),
    path(
        "cart/",
        views.cart,
        name="cart"
    ),
    path(
        "add-to-cart/<int:product_id>/",
        views.add_to_cart,
        name="add_to_cart"
    ),
    path(
        "remove-from-cart/<int:product_id>/",
        views.remove_from_cart,
        name="remove_from_cart"
    ),
    path(
        "update-cart/<int:product_id>/<str:action>/",
        views.update_cart,
        name="update_cart"
    ),
    path(
        "checkout/",
        views.checkout,
        name="checkout"
    ),
    path(
        "review/<int:product_id>/",
        views.add_review,
        name="add_review"
    ),
    path(
        "edit-store/<int:store_id>/",
        views.edit_store,
        name="edit_store"
    ),
    # Allow a vendor to delete one of their stores
    path(
        "delete-store/<int:store_id>/",
        views.delete_store,
        name="delete_store"
    ),
    # Allow vendors to edit their products
    path(
        "edit-product/<int:product_id>/",
        views.edit_product,
        name="edit_product"
    ),
    path(
        "delete-product/<int:product_id>/",
        views.delete_product,
        name="delete_product"
    ),
    # Allow a vendor to delete one of their products
    path(
        "delete-product/<int:product_id>/",
        views.delete_product,
        name="delete_product"
    ),

]
