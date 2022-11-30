from django.shortcuts import render,redirect
from django.http import HttpResponse 
from .models import registration,login,Address
from cart.models import product
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from random import randint, randrange
import uuid
import requests
import json



class user_data_object():
    def __init__(self,email,name):
        self.email = email
        self.name = name

class dash_product():
    def __init__(self,product_name,product_id,price,quantity,img):
        self.product_name = product_name
        self.product_id = product_id
        self.price = price
        self.quantity =quantity
        self.img=img

def home(request):
    object_list = []
    try:
        data = product.objects.all()[:3]
    except:
        print("not loaded")
    else:
        for x in data:
            ob = dash_product(x.product_name,x.product_id,x.price,x.quantity,x.image)
            print(ob.img.url)
            object_list.append(ob)
    if not request.session.has_key('user_login_user_id'):
        context={
            "data1":object_list,
        }
        return render(request,'registeration/navbar.html',context)
    user_id= request.session['user_login_user_id']
    try:
        data_obj = registration.objects.get(email=user_id)
    except:
        return redirect('/')
    else:
        user_obj = user_data_object(data_obj.email,data_obj.name )
        context={
            "data1":object_list,
            "data":user_obj,
        }
        return render(request,'registeration/navbar.html',context)

    


def contact(request):
    if not request.session.has_key('user_login_user_id'):
        if request.method == 'POST':
            name = request.POST.get('name')
            email = request.POST.get('email')
            subject = request.POST.get('subject')
            message = request.POST.get('message')
            send_mail_contact_us(email , name, subject,message )
            messages.success(request,'Thank You for contacting us! We will get back to you soon')
        return render(request,'registeration/contact.html')
    user_id= request.session['user_login_user_id']
    try:
        data_obj = registration.objects.get(email=user_id)
    except:
        return redirect('/contact')
    else:
        user_id= request.session['user_login_user_id']
        user_obj = user_data_object(data_obj.email,data_obj.name )
        context={
            "data":user_obj,
        }
        if request.method == 'POST':
            name = request.POST.get('name')
            email = request.POST.get('email')
            subject = request.POST.get('subject')
            message = request.POST.get('message')
            send_mail_contact_us(email , name, subject,message )
            messages.success(request,'Thank You for contacting us, We will get back to you soon')
        return render(request, 'registeration/contact.html',context)



def signup(request):
    if request.session.has_key('user_login_user_id'):
        return redirect('logout')
    if request.method == 'POST' and request.POST.get('signup'):
        name  = request.POST.get('name')
        email = request.POST.get('email')
        email.lower()
        password = make_password(request.POST.get('password'))
        phone = request.POST.get('phone')
        try:
            data = registration.objects.get(email=email)
        except:
            auth_token =str(uuid.uuid4())
            NewUserObject = registration(name = name, email = email,phone = phone,auth_token=auth_token)
            NewUserObject.save()
            data = registration.objects.get(email=email);
            NewLoginObject = login(email=data,password=password)
            NewLoginObject.save()
            send_mail_after_registration(email,auth_token)
            messages.success(request,'We have sent you verification link please verify your account')
            return redirect('/login')
        else:
            context ={
                "msg":"user already exists",
            }
            messages.success(request,'User already exists Please verify Your Account')
            return render(request,'registeration/signup.html',{})
    return render(request,'registeration/signup.html',{})




def login1(request):
 
    try:
        del request.session['user_login_user_id']
    except:
        pass
    if request.session.has_key('user_login_user_id'):
        context = {
            "user_id":request.session['user_login_user_id'],
        }
        return render(request,'',{})
    if request.method == 'POST' and request.POST.get('login'):
        email = request.POST.get('email')
        password = request.POST.get('password')
        email.lower()
        try:
            data = registration.objects.get(email=email)    
        except:
            messages.error(request, 'User not found')
            print("user not found")
        else:
            print(data.is_verified)
            if data.is_verified:
                password = str(login.objects.get(email=data).password)
                usdp=str(request.POST.get('password'))
                if  check_password(usdp,password):
                    #login success
                    request.session['user_login_user_id'] = email
                    print("logged in")
                    context={
                        "user_id":email,
                    }
                    return redirect('/')
                #return render(request,'registeration/navbar.html', context)
                else:
                    
                    context={
                        "msg":"password not correct",
                    }
                messages.error(request, 'Incorrect Password')
                return redirect('/login')
            else:
                messages.error(request,'Account not verified')
                return render(request,'registeration/login.html')

        return render(request,'registeration/login.html')
    return render(request,'registeration/login.html',{})




def logout(request):
    try:
        del request.session['user_login_user_id']
    except:
        pass
    else:
        return redirect('/login')




class user_profile():
    def __init__(self,name,email,phone):
        self.name=name
        self.email=email
        self.phone=phone



def profile(request):
    if not request.session.has_key('user_login_user_id'):
        return redirect('/login')
    if request.session.has_key('user_login_user_id'):
        user_id = request.session['user_login_user_id']
        try:
            data = registration.objects.get(email=user_id)
        except:
            print("can not load")
        else:
            ob = user_profile(data.name,data.email,data.phone)
        context = {
            "data":ob,
        }
        return render(request,'registeration/profile.html',context)
        
    


def change_profile(request):
    user_obj = user_profile("","","")
    if not request.session.has_key('user_login_user_id'):
        return redirect('/login')
    if request.session.has_key('user_login_user_id'):
        user_id= request.session['user_login_user_id']
        name = registration.objects.get(email=user_id).name
        phone = registration.objects.get(email=user_id).phone
        user_obj = user_profile(name,user_id,phone)
        context={
            "data":user_obj,
        } 
    if request.session.has_key('user_login_user_id') and request.GET.get('updateProfile'):
        user_id = request.session['user_login_user_id']
        name = request.GET.get('name')
        phone= request.GET.get('phone')
        data = registration.objects.get(email=user_id)
        data.name =name
        data.phone =phone
        data.save()
        return redirect('/profile')
    return render(request,'registeration/edit_profile.html',context)


class address_obj():
    def __init__(self,address,city,pincode,address_id):
        self.address = address
        self.city = city
        self.pincode = pincode
        self.address_id = address_id



def get_pin_code(pinc):
    endpoint="https://api.postalpincode.in/pincode/"
    pincode1 = pinc
    response = requests.get(endpoint+pincode1)
    pincode_information = json.loads(response.text)
    neccessary_information = pincode_information[0]['Status']
    if neccessary_information == "Success":
        return True
    else:
        return False



def get_state(pinc):
    endpoint="https://api.postalpincode.in/pincode/"
    pincode1 = pinc
    response = requests.get(endpoint+pincode1)
    pincode_information = json.loads(response.text)
    neccessary_information = pincode_information[0]['PostOffice'][0]['State']
    
    #print(neccessary_information)
    return str(neccessary_information)

def get_country(pinc):
    endpoint="https://api.postalpincode.in/pincode/"
    pincode1 = pinc
    response = requests.get(endpoint+pincode1)
    pincode_information = json.loads(response.text)
    neccessary_information = pincode_information[0]['PostOffice'][0]['Country']
    
    #print(neccessary_information)
    return str(neccessary_information)
def add_new_address(request):
    if not request.session.has_key('user_login_user_id'):
        return redirect('/login')
        pass

    print(request.GET.get('add_new_address'))
    if request.session.has_key('user_login_user_id') and request.GET.get('add_new_address'):
        user_id = request.session['user_login_user_id']
        flat = request.GET.get('flat')
        area = request.GET.get('area')
        city = request.GET.get('city')
        pincode = str(request.GET.get('pincode'))
        if get_pin_code(pincode):
            data = registration.objects.get(email =user_id)
            state = str(get_state(pincode))
            country= str(get_country(pincode))
            new_address_object = Address(email=data,flat= flat,area=area,city=city,pincode=pincode,state=state,country=country)
            new_address_object.save()
    return render(request,'registeration/New_Address.html',{})



def changeAddress(request):
    if request.session.has_key('user_login_uesr_id') and request.GET.get('updateaddress'):
        address = request.GET.get('address')
        city = request.GET.get('city')
        pincode = request.GET.get('pincode')
        address_id = request.GET.get('address_id')
        data_obj = Address.objects.get(address_id=address_id)
        
        data_obj.address=address
        data_obj.city =city
        data_obj.pincode =pincode

        data_obj.save()
    if request.session.has_key('user_login_user_id'):
        user_id = request.session['user_login_user_id']
        data1 = registration.objects.get(email =user_id)
        obj_list=[]
        data = Address.objects.filter(email=data1)
        for x in data:
            obj = address_obj(x.address,x.city,x.pincode)
            # print(x.address)
            obj_list.append(obj)
        context = {
            "data":obj_list,
        }
        return HttpResponse("hello")
        
#change password
def change_password(request):
    user_obj = user_data_object("","")
    if request.session.has_key('user_login_user_id'):
        user_id= request.session['user_login_user_id']
        name = registration.objects.get(email=user_id).name
        user_obj = user_data_object(user_id,name)
        context={
            "data":user_obj,
        }
    if request.session.has_key('user_login_user_id') and request.POST.get('changepassword'):
        user_id = request.session['user_login_user_id']
        old_password = str(request.POST.get('old_password'))
        new_password = str(request.POST.get('new_password'))
        data = registration.objects.get(email= user_id)
        account_password = str(login.objects.get(email=data).password)
        if check_password(old_password,account_password):
            user = login.objects.get(email=data)
            user.password = make_password(new_password)
            user.save()
            return redirect('/logout')
        else:
            return render(request)
    return render(request,'registeration/edit_password.html',context)
        
def logout(request):
    try:
        del request.session['user_login_user_id']
    except:
        pass
    else:
        return redirect('/login')



def send_mail_after_registration(email , token):
    subject = 'Your accounts need to be verified'
    message = f'Hi paste the link to verify your account http://127.0.0.1:8000/verify/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message , email_from ,recipient_list )




def verify(request , auth_token):
    try:
        profile_obj = registration.objects.filter(auth_token = auth_token).first()
    

        if profile_obj:
            if profile_obj.is_verified:
                messages.success(request, 'Your account is already verified.')
                return redirect('/accounts/login')
            profile_obj.is_verified = True
            profile_obj.save()
            messages.success(request, 'Your account has been verified.')
            return redirect('/login')
        else:
            return redirect('/error')
    except Exception as e:
        print(e)
        return redirect('/')



def send_mail_contact_us(email , name, subject,message ):
    subject = subject + ' ' +name 
    message = str(message) + '\n' +'name = ' + name + '\n email = ' + email
    
    email_id = email
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [settings.EMAIL_GET_USER]
    send_mail(subject, message , email_from ,recipient_list )


def send_mail_forgot_password( name,email,token):
    email_id = email
    subject="Password reset"
    message = "Your OTP : " + token
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email_id]
    send_mail(subject, message , email_from ,recipient_list )

def forgotPassword(request):
    if request.POST.get('forgot_password'):
        email = request.POST.get('email')
        try:
            data = registration.objects.get(email=email)
            path_token = randint(100000, 999999)
            data.path_token=path_token
            data.save()
            send_mail_forgot_password(data.name,email,path_token)
            context={
                "user_id":email,
            }
            return render(request,'registeration/CheckOtp.html',context)
        except:
            return redirect('/login')
    return render(request,'registeration/forgotpassword.html')
    

