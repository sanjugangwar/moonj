from django.shortcuts import render ,redirect
from cart.models import product,category
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.conf import settings
from django.core.mail import send_mail
from .models import *


class cate():
    def __init__(self,category_id,category_name):
        self.category_id = category_id
        self.category_name = category_name


class admin_profile():
    def __init__(self,user_id):
        self.user_id = user_id
        pass


def admin_login1(request):
    if request.method == 'POST' and request.POST.get('adminlogin'):
        user_id = request.POST.get('user_id')
        password = str(request.POST.get('password'))
        user_id.lower()
        try:
            data = admin_login.objects.get(user_id=user_id)
            object_pass = str(admin_login.objects.get(user_id=user_id).password)
            if check_password(password,object_pass):
                request.session['admin_session'] = user_id
                admin_pr = admin_profile("user_id")
                context ={
                    "data":admin_pr,
                }
                return redirect('/admin_dashboard')
        except:
            print("error")
            messages.error(request,'admin not found')
            pass
        else:
            pass
    return render(request,'registeration/admin_login.html')

def add_product(request):
    if not request.session.has_key('admin_session'):
        return redirect('/admin_login')
    if request.session.has_key('admin_session'):
        data = category.objects.all().order_by('category_name')
        obj_list =[]
        for x in data:
            obj = cate(x.category_id,x.category_name)
            obj_list.append(obj)
        context = {
            "data1":obj_list,
        }
        
    if request.session.has_key('admin_session') and request.POST.get('add_item'):
       
        product_name = request.POST.get('product_name')
        description = request.POST.get('description')
        quantity = request.POST.get('quantity')
        image = request.FILES['image']
        category_id = request.POST.get('category_id')
        price = request.POST.get('price')
        try:
            data = product.objects.get(product_name=product_name)
            if data:
                messages.success(request,'product already exists')
        except:
            categ = category.objects.get(category_id=category_id)
            try:
                obj = product(product_name = product_name,description=description,quantity=quantity,image=image,category_id=categ,price = price)
                obj.save()
                messages.success(request,'product added')

            except:
                pass
        else:
            pass
            
    return render(request,'registeration/Add_product.html',context)

# def add_product(request):
#     return render(request,'registeration/Add_product.html')
#     if not request.session.has_key('admin_session'):
#         return redirect('/admin_login')
#     if request.session.has_key('admin_session') and request.GET.get('add_item'):
#         product_name = request.GET.get('product_name')
#         description = request.GET.get('description')
#         quantity = request.GET.get('quantity')
#         image = request.GET.get('image')
#         category_id = request.GET.get('category_id')
#         price = request.GET.get('price')
#         try:
#             data = product.objects.get(product_name=product_name)
#             if data:
#                 messages.success(request,'product already exists')
#         except:
#             pass
#         else:
#             obj = product(product_name = product_name,description=description,quantity=quantity,image=image,category_id=category_id,price = price)
#             obj.save()
#             messages.success(request,'product added')


def update_product(request):
    if request.session.has_key('admin_login_id') and request.GET.get('update_product'):
        product_id = request.GET.get('product_id')
        #getting information from the user
    
        data_obj = product.objects.get(product_id=product_id)
        product_name = request.GET.get('product_name')
        description = request.GET.get('description')
        quantity = request.GET.get('quantity')
        image = request.GET.get('image')
        category_id = request.GET.get('category_id')
        price = request.GET.get('price')
        
        #updating information in objects

        data_obj.product_name = product_name
        data_obj.description = description
        data_obj.quantity = quantity
        data_obj.image = image
        data_obj.category_id = category_id
        data_obj.price =price

        #saving the object
        data_obj.save()
def add_category(request):
    
    if request.session.has_key('admin_login_id') and request.GET.get('add_category'):
        category_name = request.GET.get('category_name')
        obj = category(category_name=category_name)
        obj.save()
def update_category(request):
    if request.session.has_key('admin_login_id') and request.GET.get('update_category'):
        category_id = request.GET.get('category_id')
        obj = category.objects.get(category_id=category_id)
        category_name = request.GET.get('category_name')
        obj.category_name=category_name
        obj.save()

class profile():
    def __init__(self,user_id, name):
      self.user_id =user_id
      self.name =name
def viewProfile(request):
    if request.session.has_key('admin_login_id'):
        user_id = request.session.has_key('admin_login_id')
        user = admin_login.objects.get(user_id =user_id)
        obj = profile(user.user_id,user.name)

        context = {
            "data":obj,
        }
def update_profile(request):
    if request.session.has_key('admin_login_id'):
        user_id = request.session.has_key('admin_login_id')
        user = admin_login.objects.get(user_id =user_id)
        obj = profile(user.user_id,user.name)

        context = {
            "data":obj,
        }
    if request.session.has_key('admin_login_id') and request.GET.get('update_profile'):
        user_id = request.session['admin_login_id']
        user = admin_login.objects.get(user_id =user_id)
        # getting info from the user
        name= request.GET.get('name')
        user.name = name
        user.save()
    if request.session.has_key('admin_login_id') and request.POST.get('update_password'):
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        user_id = request.session['admin_login_id']
        data_password = str(admin_login.objects.get(user_id=user_id).password)
        
        if old_password == data_password:
            admin_object = admin_login.objects.get(user_id=user_id)
            admin_object.password = new_password
            admin_object.save()
            

 
def admin_dashboard(request):
    #return render(request,'registeration/admin_inside.html')
    admin_pr = admin_profile("")
    if not request.session.has_key('admin_session'):
        return redirect('/admin_login')
    if request.session.has_key('admin_session'):
        user_id = request.session['admin_session']
        admin_pr = admin_profile(user_id) 
        return render(request,'registeration/admin_inside.html')
    pass


def manage_tream(request):
    return render(request,'registeration/work_done.html')
    pass

class cart_object1():
    def __init__(self,sr_no,product_name,product_id,price,quantity,img):
        self.sr_no= sr_no
        self.product_name = product_name
        self.product_id = product_id
        self.price = price
        self.quantity =quantity
        self.img = img
        #self.total_price = total_price
        

def manage_product(request):
    object_list = []
    prod1 = product.objects.all().order_by('product_name')
    index=1
    for x in prod1:

           
            ob = cart_object1(index,x.product_name,x.product_id,x.price,x.quantity,x.image)
            #print(.image)           
            object_list.append(ob)
            index = index+1
    context ={
        "data1":object_list,
    }
    return render(request,'registeration/inventory_management.html',context)    
    pass
def update_inventory(request):
    # if not request.session.has_key('admin_session'):
    #     return redirect('/admin_login')
    # if request.method == "POST" and request.POST.get('update'):
    #     uid = request.GET.get('pid')
    #     try:
    #         data = product.objects.get()
    #     name = request.POST.get('product_name')
        
    return render(request,'registeration/Update_inventory.html')
    pass

class emp():
    def __init__(self,sr_no,name,salary,emp_id):
        self.sr_no = sr_no
        self.name= name
        self.salary =salary
        self.emp_id =emp_id
        pass

def employe_manage(request):
    obj_list  = []
    if request.session.has_key('admin_session'):
        data1 =  Employee.objects.all()
        index=1
        for x in data1:
            ob = emp(index,x.name,x.salary,x.employee_id)
            obj_list.append(ob)
            index =index+1
        context ={
            "data1" : obj_list,
        }
        return render(request,'registeration/employee.html',context)
    pass
def add_employe(request):
    return render(request,'registeration/Work_done.html')
    pass