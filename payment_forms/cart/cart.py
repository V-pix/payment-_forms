from decimal import Decimal

from django.conf import settings
from items.models import Item


class Cart:
    def __init__(self, request):
        """
        Initialize the cart.
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def __iter__(self):
        """
        Iterate over the items in the cart and get the items
        from the database.
        """
        item_ids = self.cart.keys()
        items = Item.objects.filter(id__in=item_ids)
        cart = self.cart.copy()
        for item in items:
            cart[str(item.id)]["item"] = item
        for item in cart.values():
            item["price"] = Decimal(item["price"])
            item["total_price"] = item["price"] * item["quantity"]
            yield item

    def __len__(self):
        """
        Count all items in the cart.
        """
        return sum(item["quantity"] for item in self.cart.values())

    def add(self, item, quantity=1, override_quantity=False):
        """
        Add a item to the cart or update its quantity.
        """
        item_id = str(item.id)
        if item_id not in self.cart:
            self.cart[item_id] = {"quantity": 0, "price": str(item.price)}
        if override_quantity:
            self.cart[item_id]["quantity"] = quantity
        else:
            self.cart[item_id]["quantity"] += quantity
        self.save()

    def save(self):
        self.session.modified = True

    def remove(self, item):
        """
        Remove a item from the cart.
        """
        item_id = str(item.id)
        if item_id in self.cart:
            del self.cart[item_id]
            self.save()

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()

    def get_total_price(self):
        return sum(
            Decimal(
                item["price"]
            ) * item["quantity"] for item in self.cart.values()
        )
