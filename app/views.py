from django import forms
from django.contrib.auth import views
from django.http import request
from django.http.response import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.views import View
from .models import Customer, Product, Cart, OrderPlaced,ContactUs
from .forms import CustomerProfileForm, CustomerRegistrationForm,LoginForm
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate,login,logout


class ProductView(View):
    def get(self, request):
        cookware = Product.objects.filter(category='C')
        electronics = Product.objects.filter(category='E')
        dinning = Product.objects.filter(category='D')
        kitchentools = Product.objects.filter(category='k')
        return render(request, 'app/home.html', {'cookware': cookware, 'electronics': electronics, 'dinning': dinning, 'kitchentools': kitchentools})


class ProductDetailView(View):
    def get(self, request,pk):
        product = Product.objects.get(pk=pk)
        return render(request, 'app/productdetail.html',{'product': product})


@login_required
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user = user, product = product).save()
    return redirect('/cart')


@login_required
def show_cart(request):
    if request.user.is_authenticated:
        user =  request.user
        cart = Cart.objects.filter(user=user)
        amount = 0.0
        shipping_amount = 100.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        # print(cart_product)
        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity * p.product.discounted_price)
                amount += tempamount
                totalamount = amount + shipping_amount
            return render(request, 'app/addtocart.html',{'carts':cart , 'totalamount': totalamount, 'amount': amount})   
        else:
            return render(request , 'app/emptycart.html')
            
def plus_cart(request):
    if request.method == 'GET':
        prod_id  = request.GET['prod_id']
        print(prod_id)
        c = Cart.objects.get(Q(product = prod_id)& Q(user = request.user))
        c.quantity += 1
        c.save()
        amount = 0.0
        shipping_amount = 0.0
        cart_product = [ p for p in Cart.objects.all() if p.user == request.user]

        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount+= tempamount
            

        
        data = {
            'quantity':c.quantity,
            'amount': amount,
            'totalamount':amount + shipping_amount
            
        }
    return JsonResponse(data)

def minus_cart(request):
    if request.method == 'GET':
        prod_id  = request.GET['prod_id']
        print(prod_id)
        c = Cart.objects.get(Q(product = prod_id)& Q(user = request.user))
        c.quantity -= 1
        c.save()
        amount = 0.0
        shipping_amount = 0.0
        cart_product = [ p for p in Cart.objects.all() if p.user == request.user]

        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount+= tempamount
           

        
        data = {
            'quantity':c.quantity,
            'amount': amount,
            'totalamount':amount + shipping_amount
            
        }
    return JsonResponse(data)

def remove_cart(request):
    if request.method == 'GET':
        prod_id  = request.GET['prod_id']
        print(prod_id)
        c = Cart.objects.get(Q(product = prod_id)& Q(user = request.user))
       
        c.delete()
        amount = 0.0
        shipping_amount = 0.0
        cart_product = [ p for p in Cart.objects.all() if p.user == request.user]

        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount+= tempamount
            

        
        data = {
           
            'amount': amount,
            'totalamount':amount + shipping_amount
            
        }
    return JsonResponse(data)

@login_required
def buy_now(request):
    return render(request, 'app/buynow.html')

@login_required
def address(request):
    add = Customer.objects.filter(user = request.user)
    return render(request, 'app/address.html', {'add':add})

def contectus(request):
    if request.method=='POST':
        fname=request.POST['fname']
        lname=request.POST['lname']
        email=request.POST['email']
        phone=request.POST['phone']
        message=request.POST['message']
        obj=ContactUs(fname=fname,lname=lname,email=email,phone=phone,message=message)
        obj.save()
        return HttpResponseRedirect('/')
    else:
        return render(request, 'app/contectform.html',)

@login_required
def orders(request):
    op = OrderPlaced.objects.filter(user = request.user)
    return render(request, 'app/orders.html', {'order_placed':op})
 

def category(request,num):
    if num == 1:
        cookware = Product.objects.filter(category = 'C') 
        name="Cookwares"
    if num == 2:
        cookware = Product.objects.filter(category = 'k') 
        name="Kitchen tools"
    if num == 3:
        cookware = Product.objects.filter(category = 'D') 
        name="Dinning and serving"
    if num == 4:
        cookware = Product.objects.filter(category = 'E') 
        name="Electronics"
        

    return render(request, 'app/category.html' ,{ 'cookware': cookware,'name':name})


def search(request):
    if request.method == 'POST':
        search=request.POST['search']
        products=Product.objects.filter(tittle__icontains=search)
        print(products)
        return render(request, 'app/category.html' ,{'cookware':products})


def CustomerRegistrationView(request):
    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Congratulation !! Registered Successfully')
            form.save()
            return HttpResponseRedirect('/userlogin')
    else:
        form = CustomerRegistrationForm
    return render(request,'app/customerregistration.html', {'form': form})


def userLogin(request):
    if request.method == 'POST':
        form=LoginForm(request=request,data=request.POST)
        if form.is_valid():
            uname=form.cleaned_data['username']
            upass=form.cleaned_data['password']
            user=authenticate(username=uname,password=upass)
            if user is not None:
                login(request,user)
                if user.is_superuser:
                    return HttpResponseRedirect('/admin')
                return HttpResponseRedirect('/profile')
    else:
        form=LoginForm()
    return render(request,'app/login.html',{'form':form})


def userLogout(request):
    logout(request)
    return HttpResponseRedirect('/')


@login_required
def checkout(request):
    user = request.user
    add = Customer.objects.filter(user = user)
    cart_items = Cart.objects.filter(user = user)
    amount = 0.0
    shipping_amount = 100
    totalamount = 0.0
    cart_product = [ p for p in Cart.objects.all() if p.user == request.user]
    if cart_product:
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount+= tempamount
        totalamount = amount+shipping_amount 
    return render(request, 'app/checkout.html',{'add' : add ,'totalamount': totalamount , 'cart_items': cart_items })

@login_required
def payment_done(request):
    user = request.user
    custid = request.GET.get('custid')
    customer = Customer.objects.get(id = custid)
    cart = Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user, customer= customer, product=c.product, quantity = c.quantity,total_price=c.total_price).save()
        c.delete()
    return redirect("orders")

@login_required
def ProfileView(request):
    obj=Customer.objects.filter(user=request.user)
    if obj:
        return HttpResponseRedirect('/')
    if request.method == 'POST':
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            usr      = request.user
            name     = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city     = form.cleaned_data['city']
            state    = form.cleaned_data['state']
            zipcode  = form.cleaned_data['zipcode']
            reg      = Customer(user=usr, name=name, locality=locality,
                           city=city, state=state, zipcode=zipcode)
            reg.save()
            # messages.success(
            #     request, 'congratulations !! profile update successfully')
            return HttpResponseRedirect('/')
    else:
        form = CustomerProfileForm()
        return render(request, 'app/profile.html', {'form': form, 'active': 'btn btn-primary'})

def discount(request):
    products=Product.objects.filter(discounted_price__gt=0)
    print(products)
    return render(request,'app/discount.html',{'products':products})

def account(request):
    if request.method == 'POST':
        num=request.POST['day']
        accounts=OrderPlaced.objects.filter(user=request.user,ordered_date__day=num)
    else:
        accounts=OrderPlaced.objects.filter(user=request.user)
    return render(request,'app/account.html',{'accounts':accounts})

