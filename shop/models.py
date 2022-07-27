from django.db import models
from django.utils import timezone

# Create your models here.
class Product(models.Model):
    product_id=models.AutoField
    product_name=models.TextField(max_length=50,default="")
    category = models.CharField(max_length=50, default="")
    subcategory=models.CharField(max_length=50,default="")
    price=models.IntegerField(default=0)
    product_desc=models.TextField(max_length=1000,default="")
    product_date=models.DateField()
    image=models.ImageField(upload_to="shop/images",default="")

    def __str__(self):
        return self.product_name
    def printdetails(self):
        return f"{self.product_name}"

class Contact(models.Model):
    msg_id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=30,default="")
    email=models.CharField(max_length=50,default="")
    phone=models.CharField(max_length=13,default="")
    date=models.DateField(default=timezone.now())
    desc=models.TextField(max_length=500,default="")

    def __str__(self):
        return self.email
class Orders(models.Model):
    order_id=models.AutoField(primary_key=True)
    items_json=models.TextField(max_length=5000)
    amount=models.IntegerField(default=0)
    name=models.CharField(max_length=60)
    email=models.CharField(max_length=60)
    address=models.CharField(max_length=200)
    date=models.DateField(default=timezone.now())
    address_line_2=models.CharField(max_length=200)
    city=models.CharField(max_length=100)
    state=models.CharField(max_length=100)
    zip_code=models.CharField(max_length=20)
    phone=models.CharField(max_length=20)

    def __str__(self):
        return f'{self.order_id} , {self.email}'

class OrderUpdate(models.Model):
    update_id=models.AutoField(primary_key=True)
    order_id=models.IntegerField(default="")
    update_desc=models.CharField(max_length=5000)
    timestamp=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.order_id},{self.update_desc[0:7]+"..."}'



