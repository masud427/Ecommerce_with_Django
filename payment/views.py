from django.shortcuts import redirect, render
from cart.cart import Cart
from payment.forms import ShippingForm, PaymentForm
from payment.models import ShippingAddress, Order, OrderItem
from django.contrib.auth.models import User
from django.contrib import messages


def process_order(request):
    if request.POST:

        # Get the cart
        cart = Cart(request)
        cart_products = cart.get_prods
        quantities = cart.get_quants
        totals = cart.cart_total()

        # Get billing info from the last page
        payment_form = PaymentForm(request.POST or None)

        # Gather Order info
        full_name= my_shipping['shipping_full_name']
        email = my_shipping['shipping_email']


        # Get shipping Session Data
        my_shipping = request.session.get('my_shipping')
        amount_paid = totals

        # Create Shipping Address from session info
        shipping_address = f"{my_shipping['shipping_address1']}\n{my_shipping['shipping_address2']}\n{my_shipping['shipping_city']}\n{my_shipping['shipping_state']}\n{my_shipping['shipping_zipcode']}\n{my_shipping['shipping_country']}"
        
        # Create an Order
        if request.user.is_authenticated:
            # Logged in
            user = request.user
            # Create Order
            create_order = Order(user= user, full_name= full_name, email= email, shipping_address=shipping_address, amount_paid= amount_paid)
            create_order.save()

            messages.success(request, "Order Placed")
            return redirect('home')

        else:
            create_order = Order(full_name= full_name, email= email, shipping_address=shipping_address, amount_paid= amount_paid)
            create_order.save() 

            messages.success(request, "Order Placed")
            return redirect('home')   


       
        

    else:
        messages.success(request, "Access Denied")
        return redirect('home')


def billing_info(request):
    if request.POST:
        # Get the cart
        cart = Cart(request)
        cart_products = cart.get_prods
        quantities = cart.get_quants
        totals = cart.cart_total()
        
        # Create a session with Shipping Info

        my_shipping = request.POST 
        request.session['my_shipping'] = my_shipping

        # check to see if user is logged in
        if request.user.is_authenticated:
            # Get the Billing form
            billing_form = PaymentForm()
            return render(request, "payment/billing_info.html",{"cart_products": cart_products, "quantities": quantities,"totals" : totals, "shipping_info":request.POST, "billing_form": billing_form })

        else:
            # not logged in
            # Get the Billing form
            billing_form = PaymentForm()
            return render(request, "payment/billing_info.html",{"cart_products": cart_products, "quantities": quantities,"totals" : totals, "shipping_info":request.POST, "billing_form": billing_form})
        
        
        shipping_form = request.POST
        return render(request, "payment/billing_info.html",{"cart_products": cart_products, "quantities": quantities,"totals" : totals, "shipping_form":shipping_form})
    else:
        messages.success(request, "Access Denied")
        return redirect('home')

def checkout(request):
    # Get the cart
    cart = Cart(request)
    cart_products = cart.get_prods
    quantities = cart.get_quants
    totals = cart.cart_total()
    if request.user.is_authenticated:
        # Check out as logged in user
        # Shipping User
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
        # Shipping Form
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
        return render(request, "payment/checkout.html",{"cart_products": cart_products, "quantities": quantities,"totals" : totals, "shipping_form":shipping_form})

    else:
       # check out as guest
       shipping_form = ShippingForm(request.POST or None)    
       return render(request, "payment/checkout.html",{"cart_products": cart_products, "quantities": quantities,"totals" : totals,"shipping_form":shipping_form})


def payment_success(request):
    return render(request, "payment/payment_success.html", {})
