from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Sum
import json

from .models import Product, User, CartItem, Order, OrderItem


def get_current_user(request):
    try:
        user_id = request.session['user_id']
        user = User.objects.get(pk=user_id)
        return user
    except KeyError:
        # default_user = User.objects.first()
        # user = default_user
        return None


def index(request):
    product_list = Product.objects.all()[:3]

    user = get_current_user(request)
    context = {
        'product_list': product_list,
        'user': user
    }
    return render(request, 'ecommerce/index.html', context)


def products(request):
    product_list = Product.objects.all()

    context = {
        'product_list': product_list,
        'user': get_current_user(request)
    }
    return render(request, 'ecommerce/products.html', context)


def login_page(request):
    return render(request, 'ecommerce/login.html')


def log_in(request):
    username = request.POST['username']
    password = request.POST['password']
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return render(request, 'ecommerce/login.html', {"error": "User doesn't exist."})

    if user.password == password:
        request.session['user_id'] = user.id
        return redirect("/ecommerce")
    else:
        return render(request, 'ecommerce/login.html', {"error": "Wrong password."})


def sign_out(request):
    del request.session['user_id']
    return redirect("/ecommerce")


def signup_page(request):
    return render(request, 'ecommerce/signup.html')


def create_user(request):
    username = request.POST['username']
    password = request.POST['password']
    confirm_password = request.POST['confirm-password']
    if password != confirm_password:
        return render(request, 'ecommerce/signup.html', {"error": "The password confirmation does not match."})

    try:
        User.objects.get(username=username)
        return render(request, 'ecommerce/signup.html', {"error": "Username already exists. Please try again."})
    except User.DoesNotExist:
        User.objects.create(username=username, password=password)
        return login_page(request)


def cart(request):
    user = get_current_user(request)
    item_list = CartItem.objects.filter(user=user.id)

    context = {
        'item_list': item_list,
        'user': user
    }
    return render(request, 'ecommerce/cart.html', context)


def product(request, product_id):
    user = get_current_user(request)
    try:
        product = Product.objects.get(pk=product_id)
    except Product.DoesNotExist:
        raise Http404("Product does not exist")
    context = {
        'product': product,
        'user': user
    }
    return render(request, 'ecommerce/detail.html', context)


def add_to_cart(request):
    user = get_current_user(request)
    user_id = user.id
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
            user=user,
            firstname=request.POST['firstname'],
            email=request.POST['email'],
            address=request.POST['address'],
            city=request.POST['city'],
            state=request.POST['state'],
            zip=request.POST['zip'],
            cardname=request.POST['cardname'],
            cardnumber=request.POST['cardnumber'],
            expmonth=request.POST['expmonth'],
            totals=request.POST['totals'],
            times=request.POST['times'],
            status=request.POST['status'],
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


def orders(request):
    user = get_current_user(request)
    order_list = Order.objects.filter(user=user.id)
    order_detail = {}
    ordersNum = 0


    for orders in order_list:
        items = OrderItem.objects.filter(order=orders.id)
        order_detail[orders] = items
        ordersNum = ordersNum + 1 


    context = {
        'order_list': order_list,
        'order_detail': order_detail,
        'ordersNum': ordersNum,
        'user': user
    }
    return render(request, 'ecommerce/orders.html', context)
