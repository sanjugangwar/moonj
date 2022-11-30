from django.db import models
from registration.models import registration
from  datetime import datetime
# Create your models here.
class category(models.Model):
    category_name = models.CharField(max_length=50)
    category_id = models.AutoField(primary_key=True)

class product(models.Model):
    product_name = models.CharField(max_length=500)
    product_id = models.AutoField(primary_key=True)
    description = models.TextField(null=True)
    quantity = models.IntegerField(default=0)
    image =  models.ImageField(upload_to="myimage",null=True)
    category_id = models.ForeignKey(category,on_delete=models.CASCADE)
    price = models.IntegerField()

class cart(models.Model):
    product_transaction_id = models.AutoField(primary_key=True)
    email = models.ForeignKey(registration,on_delete=models.CASCADE)
    product_id = models.ForeignKey(product,on_delete=models.CASCADE)
    quantity = models.IntegerField()
    time = models.TimeField(auto_now=True,null=True)




class trasaction(models.Model):
    trasaction_id = models.AutoField(primary_key=True)
    email = models.ForeignKey(registration,on_delete=models.CASCADE)
    #product_transaction_id = models.ForeignKey(cart,on_delete=models.CASCADE)
    status = models.IntegerField()
    time = models.TimeField(auto_now=True,null=True)

class user_orders(models.Model):
    email = models.ForeignKey(registration,on_delete=models.CASCADE)
    time = models.TimeField(auto_now=True)
    product_id = models.ForeignKey(product,on_delete=models.CASCADE)
    price =models.IntegerField()
    quantity= models.IntegerField()
    status  = models.BooleanField(default=False)
    razor_pay_trans_id = models.CharField(max_length=500,null=True)