from django.http import HttpResponse
from django.http import Http404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, get_object_or_404

from .models import Product, User, CartItem


def index(request):
    product_list = Product.objects.all()
    default_user = User.objects.first()

    context = {
        'product_list': product_list,
        'user': default_user
    }
    return render(request, 'ecommerce/index.html', context)


def cart(request, user_id):
    user = User.objects.get(pk=user_id)
    item_list = CartItem.objects.filter(user=user_id)

    context = {
        'item_list': item_list,
        'user': user
    }
    return render(request, 'ecommerce/cart.html', context)


def product(request, product_id):
    try:
        product = Product.objects.get(pk=product_id)
    except Product.DoesNotExist:
        raise Http404("Product does not exist")
    context = {
        'product': product,
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
