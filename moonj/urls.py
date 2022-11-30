"""moonj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from registration import views as res
from cart import views as car
from admin1 import views as admin1
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',res.home),
    path('logout/',res.logout),
    path('login/',res.login1),
    path('signup/',res.signup),
    path('product/',car.dashboard),
    path('add_to_cart/',car.add_to_cart),
    path('contact/',res.contact),
    path('cart/',car.cart1),
    path('remove_from_cart/',car.remove_from_cart),
    path('checkout/',car.checkout),
    path('orders/',car.orders),
    path('profile',res.profile),
    path('add_new_address/',res.add_new_address),
    path('edit_your_profile/',res.change_profile),
    path('change_password/',res.change_password),
    path('verify/<auth_token>',res.verify),
    path('admin_login/',admin1.admin_login1),
    path('admin_dashboard/',admin1.admin_dashboard),
    path('add_product/',admin1.add_product),
    path('manage_team/',admin1.manage_tream),
    path('update_inventory/<pid>',admin1.update_inventory),
    path('order_summary/',car.order_summary),
    path('manage_product/',car.manage_product),
    path('inventory_management/',admin1.manage_product),
    path('employe_manage/',admin1.employe_manage),
    path('add_employe/',admin1.add_employe),
    path('success/',car.success),
    path('removeCart/',car.removeCart),
    path('forgotPassword/',res.forgotPassword),


    # path('order_summary')


] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

