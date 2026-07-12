from django.test import TestCase

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User, Group

# Import the models we want to test
from .models import Store, Product, Review, Order, OrderItem


class EcommerceTestCase(TestCase):
    """
    Tests for the eCommerce application.

    These tests check that the main Part 1 functionality
    is working correctly.
    """

    def setUp(self):
        """
        Create test data before each test runs.
        """

        # Create a normal customer account
        self.customer = User.objects.create_user(
            username="customer",
            password="password123"
        )

        # Create a vendor account
        self.vendor = User.objects.create_user(
            username="vendor",
            password="password123"
        )

        # Create the Vendor group
        vendor_group = Group.objects.create(
            name="Vendor"
        )

        # Add vendor user to Vendor group
        self.vendor.groups.add(vendor_group)

        # Create a test store
        self.store = Store.objects.create(
            name="Test Store",
            description="A test online store",
            owner=self.vendor
        )

        # Create a test product
        self.product = Product.objects.create(
            store=self.store,
            name="Test Product",
            description="A product used for testing",
            price=100,
            stock=10
        )

        # Create the Django test client
        self.client = Client()


    def test_home_page_loads(self):
        """
        Test that the home page loads successfully.
        """

        response = self.client.get(
            reverse("home")
        )

        # Check that the page loads
        self.assertEqual(
            response.status_code,
            200
        )


    def test_products_page_loads(self):
        """
        Test that the products page loads successfully.
        """

        response = self.client.get(
            reverse("products")
        )

        self.assertEqual(
            response.status_code,
            200
        )


    def test_product_created_correctly(self):
        """
        Test that a product is saved correctly.
        """

        product = Product.objects.get(
            name="Test Product"
        )

        self.assertEqual(
            product.price,
            100
        )

        self.assertEqual(
            product.stock,
            10
        )


    def test_add_to_cart(self):
        """
        Test that a product can be added to the cart.
        """

        response = self.client.get(
            reverse(
                "add_to_cart",
                args=[self.product.id]
            )
        )

        # Check redirect happened
        self.assertEqual(
            response.status_code,
            302
        )

        # Check session cart contains product
        session = self.client.session

        self.assertIn(
            str(self.product.id),
            session["cart"]
        )


    def test_cart_quantity_increases(self):
        """
        Test that increasing cart quantity works.
        """

        session = self.client.session

        # Add product manually to cart
        session["cart"] = {
            str(self.product.id): 1
        }

        session.save()

        response = self.client.get(
            reverse(
                "update_cart",
                args=[
                    self.product.id,
                    "increase"
                ]
            )
        )

        self.assertEqual(
            response.status_code,
            302
        )

        # Check quantity increased
        self.assertEqual(
            self.client.session["cart"][str(self.product.id)],
            2
        )


    def test_review_creation(self):
        """
        Test that a customer can create a review.
        """

        review = Review.objects.create(
            product=self.product,
            user=self.customer,
            rating=5,
            comment="Great product!",
            verified_purchase=True
        )

        self.assertEqual(
            review.rating,
            5
        )

        self.assertEqual(
            review.comment,
            "Great product!"
        )


    def test_order_creation(self):
        """
        Test that orders and order items can be created.
        """

        order = Order.objects.create(
            customer=self.customer,
            total=100
        )

        order_item = OrderItem.objects.create(
            order=order,
            product=self.product,
            quantity=1,
            price=self.product.price
        )

        self.assertEqual(
            order.total,
            100
        )

        self.assertEqual(
            order_item.quantity,
            1
        )


    def test_vendor_login(self):
        """
        Test that a vendor can login successfully.
        """

        login = self.client.login(
            username="vendor",
            password="password123"
        )

        self.assertTrue(
            login
        )

