from django.db import models


class User(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=26)

    def __str__(self):
        return self.username


class Product(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    price = models.FloatField(null=True)
    stock = models.IntegerField(null=True)

    def __str__(self):
        return self.name


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    count = models.IntegerField()
    total = models.FloatField(null=True)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    firstname = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zip = models.CharField(max_length=50)
    cardname = models.CharField(max_length=50)
    cardnumber = models.CharField(max_length=50)
    expmonth = models.CharField(max_length=500)
    totals = models.FloatField(null=True)
    times = models.CharField(max_length=50, null=True)
    status = models.CharField(max_length=50, null=True)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    count = models.IntegerField()
    total = models.FloatField(null=True)
