from decimal import Decimal
from store.models import Product

class Cart():
    def __init__(self, request):
        self.session = request.session
         
        # Get the current session key it its exists
        cart = self.session.get('session_key')

        # If the users is new, no session key! Create one1
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}


        # cart is available in all pages
        self.cart = cart 

    def add(self, product, quantity):
        product_id = str(product.id)
        product_qty = str(quantity)
 
        # Logic
        if product_id in self.cart:
            pass
        else:
            #self.cart[product_id] = {'price' : str(product.price)}
            self.cart[product_id] = int(product_qty)       

        self.session.modified = True

    def cart_total(self):
        # Get products IDS
        product_ids = self.cart.keys()
        # lookup those keys in our products databse model
        products = Product.objects.filter(id__in = product_ids)
        # Get quantities
        quantities = self.cart
        # starting counting at 0
        total = 0

        for key, value in quantities.items():

            key = int(key)
            for product in products:
                if product.id == key:
                    if product.is_sale:
                        total = total + (product.sale_price *  Decimal(value))
                    else:
                        total = total + (product.price * Decimal(value) )    

        return total


    def __len__(self):
        return len(self.cart) 

    def get_prods(self):
        # Get ids from cart

        products_ids = self.cart.keys()

        # Use ids to lookup products in database mode
        products = Product.objects.filter (id__in = products_ids)  

        return products
    

    def get_quants(self):

        quantities = self.cart
        return quantities

    def update(self,product, quantity):
        product_id = str(product)
        product_qty = quantity

        #get cart
        ourcart = self.cart

        # update Dictionary / cart

        ourcart[product_id] = product_qty

        self.session.modified = True

        thing = self.cart

        return thing
    

    def delete(self,product):
        product_id = str(product)

        # Delete From dictionary/cart
        if product_id in self.cart:
            del self.cart[product_id]


        self.session.modified = True 

