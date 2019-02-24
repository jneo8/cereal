from django.shortcuts import render
from .models import Order

# Create your views here.

def index(request, *args, **kwargs):
    return render(
        request,
        "order/index.html",
        {
            "zero_shipping_pct": Order.zero_shipping_pct(),
        }
    )
