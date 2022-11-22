from django.urls import path

from . import views
from .views import payment_completed, payment_process

app_name = "orders"


urlpatterns = [
    path("create/", views.order_create, name="order_create"),
    path("process/", views.payment_process, name="process"),
    path("completed/", views.payment_completed, name="completed"),
    path('canceled/', views.payment_canceled, name='canceled'),
]
