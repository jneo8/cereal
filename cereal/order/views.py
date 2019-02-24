from django.shortcuts import render
from .models import Order

# Create your views here.

def gen_zero_shipping_pct_data():
    zero_shipping_pct = Order.zero_shipping_pct()
    return [
        {
            "name": "zero",
            "y": zero_shipping_pct[0],
        },
        {
            "name": "not zero",
            "y": zero_shipping_pct[1],
        },
    ]

def index(request, *args, **kwargs):

    return render(
        request,
        "order/index.html",
        {
            "zero_shipping_pct": gen_zero_shipping_pct_data(),
        }
    )
