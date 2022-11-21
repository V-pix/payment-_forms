from django.urls import path

from . import views
from .views import BuyItemView, SuccessView, create_checkout_session  # CancelView,

urlpatterns = [
    path("buy/<int:pk>/", views.create_checkout_session, name="buy"),
    path("item/<int:pk>/", BuyItemView.as_view(), name="buy_item"),
    # path('cancel/', CancelView.as_view(), name='cancel'),
    path("success/", SuccessView.as_view(), name="success"),
]
