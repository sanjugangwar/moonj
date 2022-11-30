from django.db import models

class registration(models.Model):
    name = models.CharField(max_length=100, verbose_name="name")
    email = models.EmailField(max_length=254,verbose_name="email",unique=True)
    phone = models.CharField(max_length=50,verbose_name="phone")
    auth_token=models.CharField(max_length=100)
    path_token = models.CharField(max_length=100 )
    is_verified = models.BooleanField(default=False)
    def __str__(self):
        return self.name
class login(models.Model):
    email = models.ForeignKey(registration,on_delete=models.CASCADE)
    password = models.CharField(max_length=500)
    # def __str__(self):
    #     return self.email
class Address(models.Model):
    address_id = models.AutoField(primary_key=True)
    email = models.ForeignKey(registration,on_delete=models.CASCADE)
    flat = models.CharField(max_length=500,null=True)
    area = models.CharField(max_length=500,null=True)
    city = models.CharField(max_length=50 ,null=True)
    pincode = models.IntegerField(null=True)
    state = models.CharField(max_length=500,null=True)
    country = models.CharField(max_length=500,null=True)
    # def __str__(self):
    #     return self.email
