import os

import stripe
from django.conf import settings
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView

from .models import Item

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")


@csrf_exempt
def create_checkout_session(request, pk):
    if request.method == "GET":
        domain_url = "http://localhost:8000/"
        # stripe.api_key = os.getenv('STRIPE_SECRET_KEY')
        stripe.api_key = "sk_test_51M6EjiIlMRwnUYcCexRUQryA3JCMsKuqcWxlt4js4I7JiJbAzG79cZizDWzyBnawgqilsly9FT7KFnGAz5PcLFZs00uiwGfOD9"
        item = Item.objects.get(id=pk)
        try:
            checkout_session = stripe.checkout.Session.create(
                success_url=domain_url + "success?session_id={CHECKOUT_SESSION_ID}",
                cancel_url=domain_url + "cancelled/",
                payment_method_types=["card"],
                mode="payment",
                metadata={"item_id": item.id},
                line_items=[
                    {
                        "price_data": {
                            "currency": "usd",
                            "product_data": {
                                "name": item.name,
                            },
                            "unit_amount": 200,
                        },
                        "quantity": 1,
                    },
                ],
            )
            return JsonResponse({"id": checkout_session.id})
        except Exception as e:
            return JsonResponse({"error": str(e)})


class BuyItemView(TemplateView):
    template_name = "items/item.html"

    def get_context_data(self, **kwargs):
        item_id = self.kwargs["pk"]
        item = Item.objects.get(id=item_id)
        context = super(BuyItemView, self).get_context_data(**kwargs)
        context.update(
            {
                "item": item,
                "STRIPE_PUBLIC_KEY": "pk_test_51M6EjiIlMRwnUYcCYBUcDmhf97EAxVFu0lcGvEXsLux3vBislfoqR3NLL2gYcd4r824RGtgM3TucRYhrPUnKPEhR00iB1bbcJ9",
            }
        )
        return context


class SuccessView(TemplateView):
    template_name = "items/success.html"


class CancelView(TemplateView):
    template_name = "items/cancel.html"
