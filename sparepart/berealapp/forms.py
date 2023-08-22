# forms for the workers to record sales
from django.forms import ModelForm
from .models import *
#to add stock volume of a certain product.
class AddForm(ModelForm):
    class Meta:
        model=Product
        fields=['received_quantity'] # received stock for workers to edit(incoming stock)


class SaleForm(ModelForm):
    class Meta:
        model=Sale
        fields=['quantity', 'amount_received','issued_to', 'contact','branch_name','date_of_sale']
