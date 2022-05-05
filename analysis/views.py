from django.shortcuts import render
from django.contrib.auth import authenticate, login,logout
from django.http.response import HttpResponseRedirect, JsonResponse, HttpResponse
from django.views import View
from django.shortcuts import redirect, render
from django import template
from django.template import loader
from datetime import datetime
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
        total_revenue = []
        day = []
        month = []
        this_year = []
        current_date = datetime.now().date()
        d = current_date.day
        m = current_date.month
        y = current_date.year
        for x in lt:
            dt = x.__dict__
            price = dt['total_price']
            if price:
                total_revenue.append(float(price))
            if d == dt['ordered_date'].date().day:
                day.append(float(price))
            if m == dt['ordered_date'].date().month:
                month.append(float(price))
            if y == dt['ordered_date'].date().year:
                this_year.append(float(price))
        lt  = list(Product.objects.filter())
        new, final = get_products(lt)
        new = sorted(new, key=lambda d: d['Product Sold#'])
        return render(request, 'index.html',{"Revenue": sum(total_revenue), 'day': sum(day), 'month': sum(month), 'year': sum(this_year),"product": new[:5], "stats": json.dumps(final[:5]), 'total_order_placed': len(total_revenue),  'today_order': len(day), 'month_order': len(month), 'this_year_order': len(this_year)})
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
        total_order_placed = {}        
        for x in new:
            # date = datetime.strptime(str(x['ordered_date']).rsplit(",", 1)[0], '%b. %d, %Y').date()
            date = x['ordered_date'].date()
            print(x['ordered_date'].date())
            if str(date) not in total_order_placed:
                total_order_placed[str(date)] = 1
            else:
                total_order_placed[str(date)] += 1
        
        total_order_placed = dict(sorted(total_order_placed.items(), key=lambda pair: pair[0], reverse=True))
        final = []
        for key, val in total_order_placed.items():
            final.append({'date': key, 'count': val})
        return render(request, 'order_placed.html', {"Order_place": new, "stats": final})    

def get_products(lt):
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
    return new, final


def Products(request):    
    if request.user.is_superuser:
        print(request.user)
        lt  = list(Product.objects.filter())
        new, final = get_products(lt)
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