from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Product, Store, Review


class RegisterForm(UserCreationForm):
    """
    A form for registering new users.
    """
    email = forms.EmailField()
    # Add an email field to the registration form

    REAL_CHOICES = [
        ('Buyer', 'Buyer'),
        ('Vendor', 'Vendor'),
    ]

    role = forms.ChoiceField(
        choices=REAL_CHOICES,
        widget=forms.RadioSelect
    )

    class Meta:
        """
        To define the model and fields to be used in the form.
        """
        model = User
        fields = [
            'username',
            'email',
            'password1',
            'password2',
            'role'
        ]


class StoreForm(forms.ModelForm):
    """
    Form for Vendors to create a store.
    """

    class Meta:
        model = Store
        fields = [
            "name",
            "description"
        ]


class ProductForm(forms.ModelForm):
    """
    Form for Vendors to create products.
    """

    class Meta:
        model = Product
        fields = [
            "store",
            "name",
            "description",
            "price",
            "stock"
        ]


class ReviewForm(forms.ModelForm):
    """
    Form for customers to leave a product review.
    """

    class Meta:
        # Use the Review model
        model = Review

        # Display only these fields to the user
        fields = [
            "rating",
            "comment"
        ]

        # Improve the appearance of the form fields
        widgets = {
            "rating": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 1,
                    "max": 5
                }
            ),

            "comment": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4
                }
            ),
        }
