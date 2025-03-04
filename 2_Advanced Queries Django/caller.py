import os
import django
from django.db.models import Sum, Q, F

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models
from main_app.models import Product, Category, Customer, Order, OrderProduct

# Create and run queries


def product_quantity_ordered():
    result = []
    total_quantity = Product.objects.annotate(
        total=Sum('orderproduct__quantity')).filter(total__isnull=False).values('name', 'total').order_by('-total')
    for quantity in total_quantity:
        result.append(f"Quantity ordered of {quantity['name']}: {quantity['total']}")

    return '\n'.join(result)


def ordered_products_per_customer():
    result = []
    orders = Order.objects.prefetch_related(
        'orderproduct_set__product__category').order_by('id')

    for order in orders:
        result.append(f'Order ID: {order.id}, Customer: {order.customer.username}')
        for ordered_product in order.orderproduct_set.all():
            result.append(f"- Product: {ordered_product.product.name}, Category: {ordered_product.product.category.name}")

    return '\n'.join(result)


def filter_products():
    result = []
    available_products = Product.objects.filter(Q(is_available=True) & Q(price__gt=3.00)).order_by('-price', 'name')
    for product in available_products:
        result.append(f"{product.name}: {product.price}lv.")

    return '\n'.join(result)

def give_discount():
    result = []
    query = Q(is_available=True) & Q(price__gt=3.00)
    filtered_products = Product.objects.filter(query).order_by('-price', 'name')
    filtered_products.update(price=F('price') * 0.7)
    filtered_products = Product.objects.filter(is_available=True).order_by('-price', 'name')

    for reduced_price in filtered_products:
        result.append(f"{reduced_price.name}: {reduced_price.price}lv.")

    return '\n'.join(result)


print(give_discount())