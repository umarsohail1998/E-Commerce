from django.shortcuts import render
from django.contrib.auth import authenticate, login,logout
from django.http.response import HttpResponseRedirect, JsonResponse, HttpResponse
from django.views import View
from django.shortcuts import redirect, render
from django import template
from django.template import loader

from app.models import Customer, Product, Cart, OrderPlaced, ContactUs
from app.forms import CustomerProfileForm, CustomerRegistrationForm, LoginForm
import json

top_products = []


def log_out(request):
    logout(request)
    return HttpResponseRedirect('/')

def index(request):
    if request.user.is_superuser:
        print(request.user)
        lt  = list(OrderPlaced.objects.filter())
        new = []
        for x in lt:
            dt = {}
            for field in x._meta.fields:
                if field.name not in ['id', 'user']:
                   dt[field.name] =  x.serializable_value(field.name)
            new.append(dt)
        return render(request, 'index.html',{"Order_place": new})
    else:
        logout(request)
        return redirect('user_login')
    
def order_placed(request):
    if request.user.is_superuser:
        lt  = list(OrderPlaced.objects.filter())
        new = []
        for x in lt:
            dt = {}
            for key, val in x.__dict__.items():
                if key in ['customer_id']:
                    dt[key] = list(Customer.objects.filter(id=val))[0]
                elif key not in ['id', '_state','user', 'user_id']:
                    dt[key] =  val
            new.append(dt)
        print(new)
        return render(request, 'order_placed.html',{"Order_place": new})

def Products(request):
    context = {'segment': 'index'}
    html_template = loader.get_template('product.html')
    
    if request.user.is_superuser:
        print(request.user)
        lt  = list(Product.objects.filter())
        new = []
        for x in lt:
            dt = {}
            for key, val in x.__dict__.items():
                if key in ['id']:
                    dt['Product Sold#'] = len(list(OrderPlaced.objects.filter(product_id=val)))
                elif key in ['tittle', 'selling_price', 'brand', 'category']:
                    dt[key] = val
            a_list = ['tittle', 'selling_price', 'brand', 'category', 'Product Sold#']
            new.append(dict(sorted(dt.items(), key=lambda pair: a_list.index(pair[0]))))
        
        top_product_sold = {}
        for x in new:
            top_product_sold[x['tittle']] = x['Product Sold#']
        top_product_sold = dict(sorted(top_product_sold.items(), key=lambda pair: pair[1], reverse=True))
        final =[]
        for x, y in top_product_sold.items():
            print(x, y)
            dt = {}
            dt['key'] = x
            dt['val'] = y
            final.append(dt)
        print(final)
        # top_products = top_product_sold
        return render(request, 'product.html',{"product": new, "stats": json.dumps(final)})


def Customers(request):
    if request.user.is_superuser:
        lt  = list(Customer.objects.filter())
        new = []
        for x in lt:
            dt = {}
            for key, val in x.__dict__.items():
                if key in ['id']:
                    dt['Total Order Placed'] = len(list(OrderPlaced.objects.filter(customer_id=val)))
                elif key not in ['_state', 'id', 'user_id', 'zipcode', 'state']:
                    dt[key]=val
                    
            a_list = ['name', 'locality', 'city', 'Total Order Placed']
            new.append(dict(sorted(dt.items(), key=lambda pair: a_list.index(pair[0]))))
        
        top_customers = {}
        for x in new:
            top_customers[x['name']] = x['Total Order Placed']                
        top_cust_ = dict(sorted(top_customers.items(), key=lambda pair: pair[1], reverse=True))
        final = []
        for x, y in top_cust_.items():
            print(x, y)
            dt = {}
            dt['key'] = x
            dt['val'] = y
            final.append(dt)
        print({"Customers": new, 'stats': final})
        return render(request, 'customer.html',{"Customers": new, 'stats': final})

def user_login(request):
    if request.method == 'POST':
        print(request.POST)
        form=LoginForm(request=request,data=request.POST)
        if form.is_valid():
            uname=form.cleaned_data['username']
            upass=form.cleaned_data['password']
            user=authenticate(username=uname,password=upass)
            if user.is_superuser:
                print("pas")
                login(request,user)
                return redirect('/Analysis')
    elif request.user.is_superuser:
        return redirect('/Analysis')
    else:
        form=LoginForm()
    return render(request,'login.html',{'form':form})



# Dashboard
# Revenues with month, days, years, try
# Total Products Sold by month, days
# Top 3 sold products
# Product Categories
# Which Category Is sold mostly
# Total Customer
# Total Order placed so far,
# Total products
# Total Categories