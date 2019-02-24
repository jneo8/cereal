import logging
from django.shortcuts import render
from .models import Order, OrderItem

logger = logging.getLogger(__name__)

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

def gen_hot_product_data():
    hot_items = OrderItem.hot_items(3)
    counts = []
    products = []
    for item in hot_items:
        products.append(item["product_name"])
        counts.append(item["product_count"])

    data = {
        "counts": counts,
        "names": products,
    }
    return data

def index(request, *args, **kwargs):

    return render(
        request,
        "order/index.html",
        {
            "zero_shipping_pct": gen_zero_shipping_pct_data(),
            "hot_product": gen_hot_product_data(),
        }
    )
