from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
# importing our models
from .models import *
# importing our form
from .forms import *
# importing our filters
from .filters import *
# a  decorator is an arrangement where you just reference a function but you dont call it.
from django.contrib.auth.decorators import login_required

#rrr
from django.urls import reverse


def index(request):
    return render(request,'project/index.html')


def services(request):
    return render(request,'project/services.html')

def contactus(request):
    return render(request,'project/contactus.html')

def home(request):
# querying our database and telling it to order items by id but it can be anything eg name
    products=Product.objects.all().order_by('-id')
    product_filters=ProductFilter(request.GET,queryset=products)
    products=product_filters.qs
# returning our searched data
    return render(request,'project/home.html',{'products':products,'product_filters':product_filters})



@login_required
def product_detail(request,product_id):
    product=Product.objects.get(id=product_id)
    return render(request,'project/product_detail.html',{'product':product})

    
@login_required
def receipt(request):
    sales=Sale.objects.all().order_by('-id')
    return render(request,'project/receipt.html',{'sales':sales})

@login_required 
def issue_item(request,pk):
    issued_item=Product.objects.get(id=pk)
    sales_form=SaleForm(request.POST)

    if request.method == 'POST':
        if sales_form.is_valid():
            new_sale=sales_form.save(commit=False)
            new_sale.item=issued_item
            new_sale.unit_price=issued_item.unit_price
            new_sale.save()
            #keeping track of the stock remaining after sale.
            issued_quantity=int(request.POST['quantity'])
            issued_item.total_quantity-=issued_quantity
            issued_item.save()

            print(issued_item.item_name)
            print(request.POST['quantity'])
            print(issued_item.total_quantity)

            return redirect('receipt')
    return render(request, 'project/issue_item.html',{'sales_form':sales_form})


    


def receipt_detail(request,receipt_id):
    receipt=Sale.objects.get(id=receipt_id)
    return render(request,'project/receipt_detail.html',{'receipt':receipt})


@login_required
def all_sales(request):
    sales=Sale.objects.all()
    total=sum([items.amount_received for items in sales])
    change=sum([items.get_change() for items in sales])
    net=total-change
    return render(request, 'project/all_sales.html',{'sales':sales, 'total':total, 'change':change, 'net':net})

def add_to_stock(request):
    pass

# Create your views here.
# a view is a function that responds to a url request.
# defined function must have different names.




