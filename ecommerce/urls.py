from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login_page, name='login'),
    path('log_in', views.log_in, name='log_in'),
    path('sign_out', views.sign_out, name='sign_out'),
    path('signup', views.signup_page, name='signup'),
    path('create_user', views.create_user, name='create_user'),
    path('product/<int:product_id>', views.product, name='product'),
    path('add_to_cart', views.add_to_cart, name='add_to_cart'),
    path('cart_delete_item', views.cart_delete_item, name='cart_delete_item'),
    path('cart_increase_item_count', views.cart_increase_item_count, name='cart_increase_item_count'),
    path('cart_decrease_item_count', views.cart_decrease_item_count, name='cart_decrease_item_count'),
    path('cart', views.cart, name='cart'),
    path('checkout/<int:user_id>', views.checkout, name='checkout'),
    path('products', views.products, name='products'),
    path('orders', views.orders, name='orders')
]