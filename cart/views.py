from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from .cart import Cart
from django.contrib import messages
from store.models import Product
from django.http import JsonResponse


def cart_summary(request):
    # Get the cart
    cart = Cart(request)
    cart_products = cart.get_prods
    quantities = cart.get_quants
    totals = cart.cart_total()
    return render(request, "cart_summary.html",{"cart_products": cart_products, "quantities": quantities,"totals" : totals})

def cart_add(request):
    # Get the cart
    cart = Cart(request)
   
    # test for POST
    if request.POST.get('action') == 'post':
        # Get stuff
        product_id = request.POST.get('product_id')
        if not product_id or not product_id.isdigit():
          return JsonResponse({"error": "Invalid product ID."}, status=400)
        product_qty = request.POST.get('product_qty')
        if not product_qty or not product_qty.isdigit():
          return JsonResponse({"error": "Invalid product quantity."}, status=400)

        # Convert inputs to integers
        product_id = int(product_id)
        product_qty = int(product_qty)

        # lookup products in DB
        product = get_object_or_404(Product, id = product_id )

        #save the session

        cart.add(product = product, quantity = product_qty)

        # Get Cart Qantity
        cart_quantity = cart.__len__()

        # Return response

        response = JsonResponse({'qty' : cart_quantity })
        messages.success(request, ("Product Added To Caert..."))
        return response


     


def cart_delete(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
		# Get stuff
        product_id = request.POST.get('product_id')

        # Call delete Function in Cart

        cart.delete(product= product_id)
        
        response = JsonResponse({'product':product_id})
		#return redirect('cart_summary')
        messages.success(request, ("Your Cart Has Been deleted..."))
        return response



def cart_update(request):
	cart = Cart(request)
	if request.POST.get('action') == 'post':
		# Get stuff
		product_id = request.POST.get('product_id')
		product_qty = request.POST.get('product_qty')

		cart.update(product=product_id, quantity=product_qty)

		response = JsonResponse({'qty':product_qty})
		#return redirect('cart_summary')
		messages.success(request, ("Your Cart Has Been Updated..."))
		return response