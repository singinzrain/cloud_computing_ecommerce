from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Sum

from .models import Product, User, CartItem, Order, OrderItem


def index(request):
    product_list = Product.objects.all()[:3]
    default_user = User.objects.first()

    context = {
        'product_list': product_list,
        'user': default_user
    }
    return render(request, 'ecommerce/index.html', context)


def products(request):
    product_list = Product.objects.all()
    default_user = User.objects.first()

    context = {
        'product_list': product_list,
        'user': default_user
    }
    return render(request, 'ecommerce/products.html', context)


def login(request):
    default_user = User.objects.first()

    context = {
        # 'product_list': product_list,
        # 'user': default_user
    }
    return render(request, 'ecommerce/login.html', context)


def signup(request):
    default_user = User.objects.first()

    context = {
        # 'product_list': product_list,
        # 'user': default_user
    }
    return render(request, 'ecommerce/signup.html', context)


def cart(request, user_id):
    user = User.objects.get(pk=user_id)
    item_list = CartItem.objects.filter(user=user_id)

    context = {
        'item_list': item_list,
        'user': user
    }
    return render(request, 'ecommerce/cart.html', context)


def product(request, product_id, user_id):
    try:
        user = User.objects.get(pk=user_id)
        product = Product.objects.get(pk=product_id)
    except Product.DoesNotExist:
        raise Http404("Product does not exist")
    context = {
        'product': product,
        'user': user
    }
    return render(request, 'ecommerce/detail.html', context)


def add_to_cart(request):
    user_id = request.POST['user_id']
    product_id = request.POST['product_id']
    user = get_object_or_404(User, pk=user_id)
    cart_item = CartItem.objects.filter(user=user, product_id=product_id).first()
    if cart_item is None:
        cart_item = CartItem(user=user, product_id=product_id, count=1)
    else:
        cart_item.count += 1
    cart_item.total = cart_item.product.price * cart_item.count
    cart_item.save()
    return HttpResponse('Success')


def cart_delete_item(request):
    user_id = request.POST['user_id']
    product_id = request.POST['product_id']
    user = get_object_or_404(User, pk=user_id)
    CartItem.objects.filter(user=user, product_id=product_id).delete()
    return HttpResponse('Success')


def cart_increase_item_count(request):
    user_id = request.POST['user_id']
    product_id = request.POST['product_id']
    user = get_object_or_404(User, pk=user_id)
    cart_item = CartItem.objects.filter(user=user, product_id=product_id).first()
    cart_item.count += 1
    cart_item.total = cart_item.product.price * cart_item.count
    cart_item.save()
    return HttpResponse('Success')


def cart_decrease_item_count(request):
    user_id = request.POST['user_id']
    product_id = request.POST['product_id']
    user = get_object_or_404(User, pk=user_id)
    cart_item = CartItem.objects.filter(user=user, product_id=product_id).first()
    cart_item.count -= 1
    if cart_item.count == 0:
        CartItem.objects.filter(user=user, product_id=product_id).delete()
    else:
        cart_item.total = cart_item.product.price * cart_item.count
        cart_item.save()
    return HttpResponse('Success')


def checkout(request, user_id):
    user = User.objects.get(pk=user_id)
    item_list = CartItem.objects.filter(user=user_id)
    item_sum = item_list.aggregate(Sum('total'))['total__sum']

    if request.method == 'POST' and request.POST:
        order = Order(
            firstname=request.POST['firstname'],
            email=request.POST['email'],
            address=request.POST['address'],
            city=request.POST['city'],
            state=request.POST['state'],
            zip=request.POST['zip'],
            cardname=request.POST['cardname'],
            cardnumber=request.POST['cardnumber'],
            expmonth=request.POST['expmonth'],
        )
        order.save()
        for item in item_list:
            orderItem = OrderItem(
                order=order,
                product=item.product,
                count=item.count,
                total=item.total,
            )
            orderItem.save()
            item.delete()
        return redirect('/ecommerce')

    context = {
        'item_list': item_list,
        'item_sum': item_sum,
        'product': product,
        'user': user
    }
    return render(request, 'ecommerce/checkout.html', context)
