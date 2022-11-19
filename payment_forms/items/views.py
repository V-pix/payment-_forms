from django.views.generic.base import TemplateView

class BuyItemView(TemplateView):
    template_name = 'items/item.html'
