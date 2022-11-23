import os
from decimal import Decimal

import stripe
from cart.cart import Cart
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from dotenv import find_dotenv, load_dotenv

from .forms import OrderCreateForm
from .models import Order, OrderItem

load_dotenv(find_dotenv())
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")


def order_create(request):
    cart = Cart(request)
    if request.method == "POST":
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for items in cart:
                OrderItem.objects.create(
                    order=order,
                    item=items["item"],
                    price=items["price"],
                    quantity=items["quantity"],
                )
            cart.clear()
            request.session["order_id"] = order.id
            return redirect(reverse("orders:process"))
    else:
        form = OrderCreateForm()
    return render(request, "orders/create.html", {"cart": cart, "form": form})


def payment_process(request):
    order_id = request.session.get("order_id", None)
    order = get_object_or_404(Order, id=order_id)
    if request.method == "POST":
        success_url = request.build_absolute_uri(reverse("orders:completed"))
        cancel_url = request.build_absolute_uri(reverse("orders:canceled"))
        session_data = {
            "mode": "payment",
            "client_reference_id": order.id,
            "success_url": success_url,
            "cancel_url": cancel_url,
            "line_items": [],
        }
        for item in order.items.all():
            session_data["line_items"].append(
                {
                    "price_data": {
                        "unit_amount": int(item.price * Decimal("100")),
                        "currency": "usd",
                        "product_data": {
                            "name": item.item.name,
                        },
                    },
                    "quantity": item.quantity,
                }
            )
        session = stripe.checkout.Session.create(**session_data)
        return redirect(session.url, code=303)
    else:
        return render(request, "orders/process.html", locals())


def payment_completed(request):
    return render(request, "orders/completed.html")


def payment_canceled(request):
    return render(request, "orders/canceled.html")
