from django.db import models

class admin_login(models.Model):
    admin_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    user_id = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
class Employee(models.Model):
    employee_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    bank_account = models.IntegerField()
    status = models.BooleanField(default=True)
    salary=models.IntegerField(default=0)
    def __str__(self):
        return self.name
    pass
class employee_work():
    
    pass
class Team_Management(models.Model):
    
    pass
