from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login, name='login'),
    path('signup', views.signup, name='signup'),
    path('cart/<int:user_id>/', views.cart, name='cart'),
    path('product/<int:product_id>/<int:user_id>/', views.product, name='product'),
    path('add_to_cart', views.add_to_cart, name='add_to_cart'),
    path('cart_delete_item', views.cart_delete_item, name='cart_delete_item'),
    path('cart_increase_item_count', views.cart_increase_item_count, name='cart_increase_item_count'),
    path('cart_decrease_item_count', views.cart_decrease_item_count, name='cart_decrease_item_count'),
    path('cart/<int:user_id>/', views.cart, name='cart'),
    path('checkout/<int:user_id>', views.checkout, name='checkout'),
    path('products', views.products, name='products'),
    path('orders', views.orders, name='orders')
]
