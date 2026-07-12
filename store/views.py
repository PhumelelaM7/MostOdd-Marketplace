from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect

from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test

from .models import (
    Product,
    Store,
    Order,
    OrderItem,
    Review
)

from .forms import (
    RegisterForm,
    StoreForm,
    ProductForm,
    ReviewForm
)

# Used to send emails
from django.core.mail import send_mail

# Used to retrieve the sender email from settings.py
from django.conf import settings

# Create your views here.


def home(request):
    """
    Display the homepage and all available products.
    """

    # Retrieve all Product objects from the database
    products = Product.objects.all()

    # Context dictionary to help add information
    context = {
        "products": products
    }

    # Render the home.html template located in the
    # store/templates/store directory
    return render(request, 'store/home.html', context)


def products(request):
    """
    Display the products page and all available products.
    """

    # Retrieve all Product objects from the database
    products = Product.objects.all()

    # Context dictionary to help add information
    context = {
        "products": products
    }

    # Render the products.html template located in the
    # store/templates/store directory
    return render(request, 'store/products.html', context)


def stores(request):
    """
    Displays all stores.
    """
    stores = Store.objects.all()

    context = {
        "stores": stores
    }

    return render(request, "store/stores.html", context)


def about(request):
    """
    Displays information about MostOdd Marketplace.
    """
    return render(request, "store/about.html")


def register(request):
    """
    Register a new user.
    """
    if request.method == 'POST':
        # Check if the form is submitted
        form = RegisterForm(request.POST)
        # Create an instance of the RegisterForm with the submitted data
        if form.is_valid():
            user = form.save()
            # Log in the user after successful registration
            role = form.cleaned_data["role"]
            # Add the user to the appropriate group based on their role
            group = Group.objects.get(name=role)
            # Add the user to the appropriate group based on their role
            user.groups.add(group)
            # Log in the user after successful registration
            return redirect('login')
        else:
            print(form.errors)
            # Print form errors to the console for debugging
    else:
        form = RegisterForm()
        # Create an empty instance of the RegisterForm for GET requests

    context = {  # Context dictionary to help add information
        'form': form
    }

    return render(request, 'store/register.html', context)
    # Render the register.html template located in the store
    # /templates/store directory


def login_view(request):
    """
    Log in an existing user.
    """
    if request.method == 'POST':

        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            # Log in the user if the form is valid
            user = form.get_user()
            # Get the authenticated user from the form
            login(request, user)
            # Redirect the user to the home page after successful login

            return redirect('home')
            # If the form is not valid,
            # print the errors to the console for debugging
        else:
            print(form.errors)
            # Print form errors to the console for debugging

    else:

        form = AuthenticationForm()

    context = {
        'form': form
    }

    return render(request, 'store/login.html', context)


def logout_view(request):
    """
    Log out the current user.
    """
    logout(request)  # Log out the current user
    return redirect('home')


def is_vendor(user):
    """
    Check if the user is a vendor.
    """
    return user.groups.filter(name='Vendor').exists()
    # Check if the user belongs to the 'Vendors' group


def is_buyer(user):
    """
    Check if the user is a buyer.
    """
    return user.groups.filter(name='Buyer').exists()
    # Check if the user belongs to the 'Buyers' group


@login_required
@user_passes_test(is_vendor)
def vendor_dashboard(request):
    """
    Display the vendor dashboard.
    """

    stores = Store.objects.filter(owner=request.user)

    products = Product.objects.filter(
        store__owner=request.user
    )

    context = {
        "stores": stores,
        "products": products,
    }

    return render(
        request,
        "store/vendor_dashboard.html",
        context
    )
    # Render the vendor_dashboard.html template located in the store/templates
    # /store directory


@login_required
@user_passes_test(is_vendor)
def create_store(request):
    """
    Allows Vendors to create a new store.
    """

    if request.method == "POST":
        # Check if the form is submitted

        form = StoreForm(request.POST)
        # Create an instance of the StoreForm with the submitted data

        if form.is_valid():
            # Check if the form is valid

            store = form.save(commit=False)
            # Create a new Store object without saving it to the database yet
            store.owner = request.user
            # Set the owner of the store to the currently logged-in user

            store.save()
            # Save the store to the database

            return redirect("stores")
            # Redirect the user to the stores page after successful store creation

    else:  # If the request method is not POST, create an empty form instance

        form = StoreForm()

    return render(
        request,
        "store/create_store.html",
        {
            "form": form
        }
    )


@login_required
@user_passes_test(is_vendor)
def create_product(request):
    """
    Allows Vendors to create a new product.
    """

    if request.method == "POST":
        # Check if the form is submitted

        form = ProductForm(request.POST)
        # Create an instance of the ProductForm with the submitted data

        if form.is_valid():

            product = form.save(commit=False)

            # Make sure the selected store belongs to the logged-in vendor
            if product.store.owner != request.user:
                return redirect("vendor_dashboard")

            product.save()

            return redirect("products")
            # Redirect the user to the products page
            # after successful product creation

    else:  # If the request method is not POST, create an empty form instance

        form = ProductForm()

    context = {
        "form": form
    }

    return render(request, "store/create_product.html", context)
    # Render the create_product.html template with the form context


@login_required
@user_passes_test(is_vendor)
def edit_store(request, store_id):
    """
    Allows a vendor to edit one of their stores.
    """

    store = Store.objects.get(id=store_id, owner=request.user)

    if request.method == "POST":

        form = StoreForm(request.POST, instance=store)

        if form.is_valid():

            form.save()

            return redirect("stores")

    else:

        form = StoreForm(instance=store)

    return render(
        request,
        "store/create_store.html",
        {
            "form": form
        }
    )


@login_required
@user_passes_test(is_vendor)
def delete_store(request, store_id):
    """
    Allows a vendor to delete one of their stores.
    """

    store = Store.objects.get(id=store_id, owner=request.user)

    if request.method == "POST":
        store.delete()
        return redirect("vendor_dashboard")

    return render(
        request,
        "store/delete_store.html",
        {
            "store": store
        }
    )


@login_required
@user_passes_test(is_vendor)
def edit_product(request, product_id):
    """
    Allows a vendor to edit one of their products.
    """

    product = Product.objects.get(
        id=product_id,
        store__owner=request.user
    )

    if request.method == "POST":

        form = ProductForm(
            request.POST,
            instance=product
        )

        if form.is_valid():

            form.save()

            return redirect("vendor_dashboard")

    else:

        form = ProductForm(instance=product)

    return render(
        request,
        "store/create_product.html",
        {
            "form": form
        }
    )


@login_required
@user_passes_test(is_vendor)
def delete_product(request, product_id):
    """
    Allows a vendor to delete one of their products.
    """

    product = Product.objects.get(
        id=product_id,
        store__owner=request.user
    )

    if request.method == "POST":

        product.delete()

        return redirect("vendor_dashboard")

    return render(
        request,
        "store/delete_product.html",
        {
            "product": product
        }
    )


def cart(request):
    """
    Display the user's shopping cart.
    """

    cart = request.session.get("cart", {})

    products = []

    total = 0

    for product_id, quantity in cart.items():

        product = Product.objects.get(id=product_id)

        subtotal = product.price * quantity

        total += subtotal

        products.append({
            "product": product,
            "quantity": quantity,
            "subtotal": subtotal,
        })

    context = {
        "products": products,
        "total": total,
    }

    return render(
        request,
        "store/cart.html",
        context
    )


@login_required
def add_to_cart(request, product_id):
    """
    Add a product to the shopping cart.
    """

    # Retrieve the shopping cart from the session
    cart = request.session.get("cart", {})

    # Convert the product ID to a string because
    # session keys are stored as strings
    product_id = str(product_id)

    # Retrieve the selected product
    product = Product.objects.get(id=product_id)

    # Check whether the product already exists in the cart
    if product_id in cart:

        # Only increase the quantity if stock is available
        if cart[product_id] < product.stock:
            cart[product_id] += 1

    else:

        # Only add the product if at least one item is in stock
        if product.stock > 0:
            cart[product_id] = 1

    # Save the updated cart
    request.session["cart"] = cart

    # Redirect the user to the shopping cart
    return redirect("cart")


def remove_from_cart(request, product_id):
    """
    Remove a product from the shopping cart.
    """

    cart = request.session.get("cart", {})

    product_id = str(product_id)

    if product_id in cart:
        del cart[product_id]

    request.session["cart"] = cart

    return redirect("cart")


@login_required
def update_cart(request, product_id, action):
    """
    Increase or decrease the quantity of a product in the cart.
    """

    # Retrieve the shopping cart from the session
    cart = request.session.get("cart", {})

    # Convert the product ID to a string because
    # session dictionary keys are stored as strings
    product_id = str(product_id)

    # Retrieve the product from the database
    product = Product.objects.get(id=product_id)

    # Check whether the product exists in the cart
    if product_id in cart:

        # Increase the quantity
        if action == "increase":

            # Only increase if sufficient stock is available
            if cart[product_id] < product.stock:
                cart[product_id] += 1

        # Decrease the quantity
        elif action == "decrease":

            cart[product_id] -= 1

            # Remove the product if the quantity reaches zero
            if cart[product_id] <= 0:
                del cart[product_id]

    # Save the updated cart
    request.session["cart"] = cart

    # Redirect back to the shopping cart
    return redirect("cart")


@login_required
def checkout(request):
    """
    Process the user's order, save it to the database,
    and email an invoice to the buyer.
    """

    # Retrieve the shopping cart from the user's session
    cart = request.session.get("cart", {})

    # Redirect the user back to the cart if it is empty
    if not cart:
        return redirect("cart")

    # Initialise the total cost of the order
    total = 0

    # Create a new Order object for the current user
    order = Order.objects.create(
        customer=request.user,
        total=0
    )

    # Create a list that will be used to build the invoice email
    invoice_items = []

    # Loop through each product in the shopping cart
    for product_id, quantity in cart.items():

        # Retrieve the product from the database
        product = Product.objects.get(id=product_id)

        # Check that enough stock is available
        if quantity > product.stock:
            return redirect("cart")

        # Calculate the subtotal
        subtotal = product.price * quantity

        # Add the subtotal to the order total
        total += subtotal

        # Reduce the available stock
        product.stock -= quantity

        # Save the updated stock level
        product.save()

        # Create an OrderItem
        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=quantity,
            price=product.price
        )

        # Store product information for the email invoice
        invoice_items.append({
            "name": product.name,
            "quantity": quantity,
            "price": product.price,
            "subtotal": subtotal
        })

    # Update the total cost of the order
    order.total = total

    # Save the completed order
    order.save()

    # ============================================================
    # Build the invoice email
    # ============================================================

    # Email subject
    subject = f"MostOdd Marketplace Invoice #{order.id}"

    # Greeting
    message = (
        f"Hello {request.user.username},\n\n"
        f"Thank you for shopping with MostOdd Marketplace.\n\n"
        f"Order Number: {order.id}\n\n"
        f"Items Purchased:\n\n"
    )

    # Add every purchased product to the email
    for item in invoice_items:

        message += (
            f"{item['name']}\n"
            f"Quantity: {item['quantity']}\n"
            f"Price: R{item['price']}\n"
            f"Subtotal: R{item['subtotal']}\n\n"
        )

    # Add the total amount
    message += f"Order Total: R{total}\n\n"

    # Closing message
    message += (
        "Thank you for shopping with us.\n\n"
        "MostOdd Marketplace"
    )

    # Send the email to the customer
    send_mail(
        # Subject
        subject,

        # Email body
        message,

        # Sender email
        settings.DEFAULT_FROM_EMAIL,

        # Recipient
        [request.user.email],

        # Raise an error if sending fails
        fail_silently=False
    )

    # Empty the shopping cart
    request.session["cart"] = {}

    # Display the checkout confirmation page
    return render(
        request,
        "store/checkout.html",
        {
            "order": order
        }
    )


@login_required
def add_review(request, product_id):
    """
    Allow a customer to leave a review for a product.
    """

    # Retrieve the selected product
    product = Product.objects.get(id=product_id)

    # Check whether the customer has purchased this product
    verified = OrderItem.objects.filter(
        order__customer=request.user,
        product=product
    ).exists()

    # Check whether the form has been submitted
    if request.method == "POST":

        # Populate the form with submitted data
        form = ReviewForm(request.POST)

        # Validate the submitted form
        if form.is_valid():

            # Create the Review object without saving it yet
            review = form.save(commit=False)

            # Assign the product
            review.product = product

            # Assign the logged-in user
            review.user = request.user

            # Record whether the purchase was verified
            review.verified_purchase = verified

            # Save the review
            review.save()

            # Redirect back to the products page
            return redirect("products")

    else:

        # Display an empty review form
        form = ReviewForm()

    # Render the review form
    return render(
        request,
        "store/add_review.html",
        {
            "form": form,
            "product": product,
            "verified": verified
        }
    )


@login_required
@user_passes_test(is_vendor)
def edit_store(request, store_id):
    """
    Allow a vendor to edit one of their stores.
    """

    # Retrieve the store that belongs to the logged-in vendor
    store = Store.objects.get(
        id=store_id,
        owner=request.user
    )

    # Check whether the form has been submitted
    if request.method == "POST":

        # Populate the form with the submitted data
        # and the existing store instance
        form = StoreForm(
            request.POST,
            instance=store
        )

        # Validate the form
        if form.is_valid():

            # Save the updated store information
            form.save()

            # Redirect the vendor back to the dashboard
            return redirect("vendor_dashboard")

    else:

        # Display the existing store information
        # inside the form
        form = StoreForm(instance=store)

    # Pass the form to the template
    context = {
        "form": form,
        "store": store
    }

    # Render the edit store page
    return render(
        request,
        "store/edit_store.html",
        context
    )


@login_required
@user_passes_test(is_vendor)
def delete_store(request, store_id):
    """
    Allow a vendor to delete one of their stores.
    """

    # Retrieve the store that belongs to the logged-in vendor
    store = Store.objects.get(
        id=store_id,
        owner=request.user
    )

    # Check if the confirmation form has been submitted
    if request.method == "POST":

        # Delete the store from the database
        store.delete()

        # Redirect back to the Vendor Dashboard
        return redirect("vendor_dashboard")

    # Pass the store to the template
    context = {
        "store": store
    }

    # Display the confirmation page
    return render(
        request,
        "store/delete_store.html",
        context
    )


@login_required
@user_passes_test(is_vendor)
def edit_product(request, product_id):
    """
    Allow a vendor to edit one of their products.
    """

    # Retrieve the product that belongs to one of the
    # logged-in vendor's stores
    product = Product.objects.get(
        id=product_id,
        store__owner=request.user
    )

    # Check if the form has been submitted
    if request.method == "POST":

        # Populate the form with the submitted data
        # and the existing product instance
        form = ProductForm(
            request.POST,
            instance=product
        )

        # Validate the submitted form
        if form.is_valid():

            # Save the updated product
            form.save()

            # Return the vendor to the dashboard
            return redirect("vendor_dashboard")

    else:

        # Display the current product information
        form = ProductForm(instance=product)

    # Context dictionary passed to the template
    context = {
        "form": form,
        "product": product
    }

    # Render the edit product page
    return render(
        request,
        "store/edit_product.html",
        context
    )


@login_required
@user_passes_test(is_vendor)
def delete_product(request, product_id):
    """
    Allow a vendor to delete one of their products.
    """

    # Retrieve the product that belongs to one of the
    # logged-in vendor's stores
    product = Product.objects.get(
        id=product_id,
        store__owner=request.user
    )

    # Check whether the confirmation form has been submitted
    if request.method == "POST":

        # Delete the product from the database
        product.delete()

        # Redirect back to the Vendor Dashboard
        return redirect("vendor_dashboard")

    # Context dictionary passed to the template
    context = {
        "product": product
    }

    # Display the confirmation page
    return render(
        request,
        "store/delete_product.html",
        context
    )