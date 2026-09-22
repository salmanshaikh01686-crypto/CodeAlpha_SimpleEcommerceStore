from decimal import Decimal
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CheckoutForm, RegisterForm
from .models import Order, OrderItem, Product

def cart_count(request):
    return sum(request.session.get("cart", {}).values())

def base_context(request):
    return {"cart_count": cart_count(request)}

def product_list(request):
    products = Product.objects.all()
    return render(request, "shop/product_list.html", {"products": products, **base_context(request)})

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, "shop/product_detail.html", {"product": product, **base_context(request)})

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if product.stock <= 0:
        messages.error(request, "This product is out of stock.")
        return redirect("product_detail", product_id=product.id)

    cart = request.session.get("cart", {})
    key = str(product.id)
    current = cart.get(key, 0)
    if current < product.stock:
        cart[key] = current + 1
        request.session["cart"] = cart
        messages.success(request, f"{product.name} added to cart.")
    else:
        messages.warning(request, "You cannot add more than available stock.")
    return redirect("cart")

def cart(request):
    raw_cart = request.session.get("cart", {})
    products = Product.objects.filter(id__in=raw_cart.keys())
    items = []
    total = Decimal("0.00")

    for product in products:
        quantity = raw_cart.get(str(product.id), 0)
        subtotal = product.price * quantity
        total += subtotal
        items.append({"product": product, "quantity": quantity, "subtotal": subtotal})

    return render(request, "shop/cart.html", {"items": items, "total": total, **base_context(request)})

def update_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get("quantity", 1))
    cart = request.session.get("cart", {})

    if quantity <= 0:
        cart.pop(str(product_id), None)
    else:
        cart[str(product_id)] = min(quantity, product.stock)

    request.session["cart"] = cart
    return redirect("cart")

def remove_from_cart(request, product_id):
    cart = request.session.get("cart", {})
    cart.pop(str(product_id), None)
    request.session["cart"] = cart
    return redirect("cart")

@login_required
def checkout(request):
    raw_cart = request.session.get("cart", {})
    products = Product.objects.filter(id__in=raw_cart.keys())

    if not raw_cart or not products.exists():
        messages.info(request, "Your cart is empty.")
        return redirect("product_list")

    total = Decimal("0.00")
    cart_items = []
    for product in products:
        quantity = raw_cart.get(str(product.id), 0)
        if quantity > product.stock:
            messages.error(request, f"Not enough stock for {product.name}.")
            return redirect("cart")
        total += product.price * quantity
        cart_items.append((product, quantity))

    if request.method == "POST":
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.total = total
            order.save()

            for product, quantity in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity,
                    price=product.price,
                )
                product.stock -= quantity
                product.save(update_fields=["stock"])

            request.session["cart"] = {}
            messages.success(request, f"Order #{order.id} placed successfully.")
            return redirect("orders")
    else:
        form = CheckoutForm(initial={
            "full_name": request.user.get_full_name() or request.user.username,
            "email": request.user.email,
        })

    return render(request, "shop/checkout.html", {
        "form": form,
        "cart_items": cart_items,
        "total": total,
        **base_context(request),
    })

@login_required
def orders(request):
    order_list = Order.objects.filter(user=request.user).prefetch_related("items__product")
    return render(request, "shop/orders.html", {"orders": order_list, **base_context(request)})

def register(request):
    if request.user.is_authenticated:
        return redirect("product_list")
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created successfully.")
            return redirect("product_list")
    else:
        form = RegisterForm()
    return render(request, "shop/register.html", {"form": form})

def user_login(request):
    if request.user.is_authenticated:
        return redirect("product_list")
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("product_list")
        messages.error(request, "Invalid username or password.")
    return render(request, "shop/login.html")

def user_logout(request):
    logout(request)
    return redirect("product_list")
