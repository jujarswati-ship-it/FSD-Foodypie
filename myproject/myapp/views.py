from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
from decimal import Decimal

from .models import Product


# Home Page
def home(request):
    return render(request, 'accounts/home.html')


# Products Page
def products(request):
    food_items = Product.objects.filter(is_available=True)

    return render(request, 'accounts/products.html', {
        'products': food_items,
    })


# Add to Cart
@require_POST
def add_to_cart(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id,
        is_available=True
    )

    cart = request.session.get('cart', {})

    product_id = str(product.id)

    cart[product_id] = cart.get(product_id, 0) + 1

    request.session['cart'] = cart

    return redirect('order')


# Update Cart
@require_POST
def update_cart(request, product_id):

    cart = request.session.get('cart', {})

    product_id = str(product_id)

    action = request.POST.get('action')

    if action == 'remove':

        cart.pop(product_id, None)

    elif action == 'update':

        try:
            quantity = int(request.POST.get('quantity', 1))

            if quantity > 0 and product_id in cart:
                cart[product_id] = quantity

        except (ValueError, TypeError):
            pass

    request.session['cart'] = cart

    return redirect('order')


# Get Cart Details
def get_cart_details(request):

    cart = request.session.get('cart', {})

    order_items = []

    total = Decimal('0.00')

    for product_id, quantity in cart.items():

        try:
            product = Product.objects.get(
                id=product_id,
                is_available=True
            )

            quantity = int(quantity)

            if quantity < 1:
                continue

        except (Product.DoesNotExist, ValueError, TypeError):
            continue

        subtotal = product.price * quantity

        order_items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal,
        })

        total += subtotal

    return order_items, total


# Order / Cart Page
def order_page(request):

    order_items, total = get_cart_details(request)

    return render(request, 'accounts/order.html', {
        'order_items': order_items,
        'total': total,
    })


# Checkout Page
def checkout(request):

    order_items, total = get_cart_details(request)

    if not order_items:
        return redirect('order')

    return render(request, 'accounts/checkout.html', {
        'order_items': order_items,
        'total': total,
    })


# Place Order / Order Success
def place_order(request):

    if request.method != 'POST':
        return redirect('checkout')

    order_items, total = get_cart_details(request)

    if not order_items:
        return redirect('order')

    full_name = request.POST.get('full_name', '').strip()

    email = request.POST.get('email', '').strip()

    phone = request.POST.get('phone', '').strip()

    address = request.POST.get('address', '').strip()

    city = request.POST.get('city', '').strip()

    pincode = request.POST.get('pincode', '').strip()

    payment_method = request.POST.get('payment_method', '')

    if not all([
        full_name,
        email,
        phone,
        address,
        city,
        pincode
    ]):
        return redirect('checkout')

    if payment_method not in ['cod', 'online']:
        return redirect('checkout')

    # Store order total before clearing cart
    order_total = total

    # Clear cart after order submission
    request.session['cart'] = {}

    # Display Order Success Page
    return render(request, 'accounts/order_success.html', {
        'full_name': full_name,
        'total': order_total,
        'payment_method': payment_method,
    })


# Register Page
def register_page(request):

    if request.method == "POST":

        username = request.POST.get("username")

        email = request.POST.get("email")

        password = request.POST.get("password")

        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:

            return render(request, "accounts/register.html", {
                "error": "Passwords do not match"
            })

        if User.objects.filter(username=username).exists():

            return render(request, "accounts/register.html", {
                "error": "Username already exists"
            })

        if User.objects.filter(email=email).exists():

            return render(request, "accounts/register.html", {
                "error": "Email already exists"
            })

        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        return redirect('login')

    return render(request, "accounts/register.html")


# Login Page
def login_page(request):

    if request.method == "POST":

        username = request.POST.get("username")

        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect('dashboard')

        else:

            return render(request, "accounts/login.html", {
                'error': "Invalid Username or password"
            })

    return render(request, 'accounts/login.html')


# Dashboard Page
@login_required(login_url='login')
def dashboard(request):

    return render(request, 'accounts/dashboard.html', {
        'user': request.user
    })


# Logout Page
def logout_page(request):

    if request.method == "POST":

        logout(request)

    return redirect('login')