from django.urls import path

from . import views

urlpatterns = [
    path('item/<int:pk>/', views.BuyItemView.as_view(), name='buy_item'),
]