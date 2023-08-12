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

# this view renders the index.html template and this displays the landing pages of my web appliation.
def index(request):
    return render(request,'project/index.html')

# this view renders the servises.html template and this diplays the services we offered by be real motors.
def services(request):
    return render(request,'project/services.html')

# this view renders the contactus.html template and this diplays informtion of how you get in touch with be real motors.
def contactus(request):
    return render(request,'project/contactus.html')



# querying our database and telling it to order items by id but it can be anything eg name
# line 39 fetches all the data from `the database using product model.`
# line 40 filters the products and provides us with data based on user input.

@login_required
def home(request):
# querying our database and telling it to order items by id but it can be anything eg name
# line 29 fetches all the data from `the database using product model.`
# line 30 filters the products and provides us with data based on user input.
    products=Product.objects.all().order_by('-id')
    product_filters=ProductFilter(request.GET,queryset=products)
    products=product_filters.qs
# returning our searched data/ rendering our home.html page.
    return render(request,'project/home.html',{'products':products,'product_filters':product_filters})


# This view fetches specific product from the database based on the product id parameter
# and then provides us an html pages showing the selected product.
@login_required
def product_detail(request,product_id):
    product=Product.objects.get(id=product_id)
    return render(request,'project/product_detail.html',{'product':product})

    

 # this retrieves a list of sales records from the database and then orders them by id.
 # and renders the receipt.html template which is responsible for displaying a list of sales receipts. 
@login_required
def receipt(request):
    sales=Sale.objects.all().order_by('-id')
    return render(request,'project/receipt.html',{'sales':sales})


# this handles the issuing of an item for sale.
# it fetches the specific product using pk and processes the sale using SaleForm.
# after a successful sale it redirects you to the receipt view.

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


    
# This fetches sales receipt from the database based on receipt id parameter.
# then renders a receipt_detail.html displaying detailed informtion about a selected receipt.
@login_required
def receipt_detail(request,receipt_id):
    # below is a query.
    # here we are querying all the data by id.
    receipt=Sale.objects.get(id=receipt_id)
    return render(request,'project/receipt_detail.html',{'receipt':receipt})


# This list retrieves a list of all sales records from the db and then calculates
# the total,change and net values based on the sales data.
# the results are then rendered in the all_sales.html template.
@login_required
def all_sales(request):
    # query all the data from the module Sale below on line 85.
    sales=Sale.objects.all()
    total=sum([items.amount_received for items in sales])
    change=sum([items.get_change() for items in sales])
    net=total-change
    return render(request, 'project/all_sales.html',{'sales':sales, 'total':total, 'change':change, 'net':net})



# This handles the process of adding items to the stock.
# it fetches a product using its pk and processes the addition using the AddForm and updates the stock of the product.
# After a successful adding of stock, it redirecs you to the home view.
@login_required
def add_to_stock(request,pk):
    issued_item=Product.objects.get(id=pk)
    form=AddForm(request.POST)

    if request.method=='POST':
        if form.is_valid():
            added_quantity=int(request.POST['received_quantity'])
            issued_item.total_quantity += added_quantity
            issued_item.save()
            # to add to the remaining stock quantity is reduced.
            print(added_quantity)
            print(issued_item.total_quantity)
            return redirect('home')
    return render(request, 'project/add_to_stock.html', {'form': form})

# Create your views here.
# a view is a function that responds to a url request.
# defined function must have different names.




