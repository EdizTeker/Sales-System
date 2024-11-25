from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from .models import Item, Cart
from .forms import ItemForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from django.core.paginator import Paginator
from django.shortcuts import render
from rest_framework import viewsets
from .models import *
from .serializers import ItemSerializer, CartSerializer

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer


# Create your views here.

def item_index(request):


    
    item_list = Item.objects.all()
    query = request.GET.get('q')
    if query:
        item_list = item_list.filter(name__icontains=query)


    paginator = Paginator(item_list, 6)  # Show 25 contacts per page.

    page_number = request.GET.get("page")
    items = paginator.get_page(page_number)
    return render(request, "item/index.html", {"items": items})

    #items = Item.objects.all()
    #return render(request, 'item/index.html', {'items': items})


def item_detail(request, id):

    item = get_object_or_404(Item, id=id)
    form = ItemForm(request.POST or None)
    update = 0
    
    if request.user.is_authenticated:

        update = bool(Cart.objects.filter(user=request.user, cartitem = id ))

    if request.POST.get('cartnumber') is not None:
            
            if request.user.is_authenticated:
                
                
                if form.is_valid() & (int(request.POST.get('cartnumber')) == 0):
                    
                    testt = bool(Cart.objects.filter(user=request.user, cartitem=item))
                    if (testt):
                        Cart.objects.filter(user=request.user, cartitem = id ).delete()
                        messages.success(request, 'The item has been removed.')
                        
                    else:    
                        messages.warning(request, 'Please select the number correctly')
                else:
                    if form.is_valid() & (int(request.POST.get('cartnumber')) <= item.stock):
                        
                        Cart.objects.filter(user=request.user, cartitem = id ).delete()
                        cart_to_be_added = form.save(commit=False)
                        cart_to_be_added.user = request.user
                        cart_to_be_added.cartitem = item
                        cart_to_be_added.save()
                        #return redirect('detail')
                        messages.success(request, 'The item has been added to the cart.')
                        
                        
                    else:
                        messages.warning(request, 'Please select the number correctly')
            
            elif form.is_valid():
                    
                messages.warning(request, 'Please log in.')
        
     
    

    context = {
        'item': item,
        'form': form,
        'update': update
    }
    
    return render(request, 'item/detail.html', context)


@login_required
def item_cart(request):
    
    
    user_cart_items = Cart.objects.filter(user=request.user)
    cart_items = []
    for cart_item in user_cart_items:
    
        item_details = {
            'id': cart_item.cartitem.id,
            'name': cart_item.cartitem.name,
            'category': cart_item.cartitem.category,
            'price': cart_item.cartitem.price,
            'quantity': cart_item.cartnumber,        

            'link': cart_item.cartitem.get_absolute_url    
        }

        
        cart_items.append(item_details)
    



    context = {
        
        'cart_items': cart_items,
        

        
    }




    return render(request, 'item/cart.html', context)



@login_required
def item_purchase(request):
    user_cart_items = Cart.objects.filter(user=request.user)
    
    for cart_item in user_cart_items:
        item = cart_item.cartitem
        if item.stock >= cart_item.cartnumber:
            item.stock -= cart_item.cartnumber
            item.save()
            cart_item.delete()
        else:
            messages.error(request, f"Not enough stock for {item.name}")
            return redirect('item:cart')

    messages.success(request, "Purchase successful!")
    return redirect('item:cart')
