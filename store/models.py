from django.db import models
from django.contrib.auth.models import User  # Import the User model

# Create your models here.


class Store(models.Model):
    """
    Represents a vendor's online store.
    """
    owner = models.ForeignKey(
        # Link the store to a user (vendor)
        User,
        on_delete=models.CASCADE,
        # If the user is deleted, also delete their store
        related_name="stores"
        # Allows reverse access to the user's stores
    )
    name = models.CharField(max_length=100)
    # Name of the store
    description = models.TextField()
    # Description of the store
    created_at = models.DateTimeField(auto_now_add=True)
    # Timestamp for when the store was created

    def __str__(self):
        return self.name
        # Return the store's name when the object is printed


class Product(models.Model):
    """
    Represents a product in a store.
    """

    store = models.ForeignKey(  # Link the product to the store
        Store,
        on_delete=models.CASCADE,
        related_name="products"
    )

    name = models.CharField(max_length=100)  # Name of the product
    description = models.TextField()  # Description of the product
    created_at = models.DateTimeField(auto_now_add=True)
    # Time stamp when the product was added

    price = models.DecimalField(  # Price of the product
        max_digits=10,
        decimal_places=2
    )

    stock = models.PositiveIntegerField(default=0)  # Available stock

    def __str__(self):
        return self.name  # Return the products name


class Review(models.Model):
    """
    Represents a customer's review of a product.
    """

    product = models.ForeignKey(  # Link review to the product
        Product,
        on_delete=models.CASCADE,
        related_name="reviews"

    )

    user = models.ForeignKey(  # Link review to the user
        User,
        on_delete=models.CASCADE,
        related_name="reviews"
    )

    rating = models.PositiveSmallIntegerField()  # Allow user to leave a rating
    comment = models.TextField()  # Allow user to leave a comment
    created_at = models.DateTimeField(auto_now_add=True)
    # Time stamp of the comment

    def __str__(self):
        return f"{self.product.name} - {self.user.username}"
        # Returns the product name and the username


class Order(models.Model):
    """
    Represents a completed customer order.
    """

    customer = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    total = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"Order #{self.id}"


class OrderItem(models.Model):
    """
    Represents a product within an order.
    """

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items"
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    quantity = models.PositiveIntegerField()

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def __str__(self):
        return self.product.name


class Review(models.Model):
    """
    Represents a review left by a customer for a product.
    """

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="reviews"
        # Delete reviews if the product is deleted
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
        # Delete reviews if the user is deleted
    )

    rating = models.PositiveIntegerField()
    # Rating out of 5

    comment = models.TextField()
    # Customer's written review

    verified_purchase = models.BooleanField(
        default=False
    )
    # Indicates whether the reviewer purchased the product

    created_at = models.DateTimeField(
        auto_now_add=True
    )
    # Automatically record when the review was created

    def __str__(self):
        """
        Return a readable representation of the review.
        """
        return f"{self.user.username} - {self.product.name}"