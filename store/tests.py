from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User, Group

# Import models from the store application
from .models import (
    Store,
    Product,
    Review,
    Order,
    OrderItem
)


class EcommerceTestCase(TestCase):
    """
    Test cases for the Django eCommerce application.
    """


    def setUp(self):
        """
        Create test data before each test runs.
        """

        # Create customer account
        self.customer = User.objects.create_user(
            username="customer",
            password="password123"
        )


        # Create vendor account
        self.vendor = User.objects.create_user(
            username="vendor",
            password="password123"
        )


        # Create Vendor group
        vendor_group = Group.objects.create(
            name="Vendor"
        )


        # Add vendor user to Vendor group
        self.vendor.groups.add(
            vendor_group
        )


        # Create a store owned by the vendor
        self.store = Store.objects.create(
            owner=self.vendor,
            name="Test Store",
            description="Test store description"
        )


        # Create a product inside the store
        self.product = Product.objects.create(
            store=self.store,
            name="Test Product",
            description="Test product description",
            price=100,
            stock=10
        )


        # Create test client
        self.client = Client()



    def test_home_page_loads(self):
        """
        Test that the home page loads successfully.
        """

        # Open home page
        response = self.client.get(
            reverse("home")
        )


        # Check page loads successfully
        self.assertEqual(
            response.status_code,
            200
        )



    def test_products_page_loads(self):
        """
        Test that the products page loads successfully.
        """

        # Open products page
        response = self.client.get(
            reverse("products")
        )


        # Check page loads successfully
        self.assertEqual(
            response.status_code,
            200
        )



    def test_product_created_correctly(self):
        """
        Test that products are created correctly.
        """

        # Retrieve product from database
        product = Product.objects.get(
            name="Test Product"
        )


        # Check product price
        self.assertEqual(
            product.price,
            100
        )


        # Check product stock
        self.assertEqual(
            product.stock,
            10
        )



    def test_add_to_cart(self):
        """
        Test that a product can be added to the cart.
        """


        # Login customer before accessing cart features
        self.client.login(
            username="customer",
            password="password123"
        )


        # Add product to cart
        response = self.client.get(
            reverse(
                "add_to_cart",
                args=[
                    self.product.id
                ]
            )
        )


        # Check redirect to cart page
        self.assertEqual(
            response.status_code,
            302
        )


        # Reload session
        session = self.client.session


        # Check product exists in cart
        self.assertEqual(
            session["cart"][str(self.product.id)],
            1
        )



    def test_update_cart(self):
        """
        Test that cart quantity can be increased.
        """


        # Login customer
        self.client.login(
            username="customer",
            password="password123"
        )


        # Create starting cart session
        session = self.client.session

        session["cart"] = {
            str(self.product.id): 1
        }


        # Save session changes
        session.save()



        # Increase cart quantity
        response = self.client.get(
            reverse(
                "update_cart",
                args=[
                    self.product.id,
                    "increase"
                ]
            )
        )


        # Check redirect response
        self.assertEqual(
            response.status_code,
            302
        )


        # Reload session
        session = self.client.session



        # Confirm quantity increased
        self.assertEqual(
            session["cart"][str(self.product.id)],
            2
        )



    def test_review_creation(self):
        """
        Test that a customer can create a product review.
        """

        # Create review
        review = Review.objects.create(
            product=self.product,
            user=self.customer,
            rating=5,
            comment="Great product",
            verified_purchase=True
        )


        # Check review rating
        self.assertEqual(
            review.rating,
            5
        )



    def test_order_creation(self):
        """
        Test that orders and order items are created.
        """

        # Create order
        order = Order.objects.create(
            customer=self.customer,
            total=100
        )


        # Add product to order
        order_item = OrderItem.objects.create(
            order=order,
            product=self.product,
            quantity=1,
            price=100
        )


        # Check order total
        self.assertEqual(
            order.total,
            100
        )


        # Check order item quantity
        self.assertEqual(
            order_item.quantity,
            1
        )



    def test_vendor_login(self):
        """
        Test that a vendor can login successfully.
        """

        # Attempt login
        login_successful = self.client.login(
            username="vendor",
            password="password123"
        )


        # Confirm login worked
        self.assertTrue(
            login_successful
        )