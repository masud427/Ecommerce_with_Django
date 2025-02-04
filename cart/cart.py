from decimal import Decimal
from store.models import Product, Profile

class Cart():
    def __init__(self, request):
        self.session = request.session
        # Get request
        self.request = request
         
        # Get the current session key it its exists
        cart = self.session.get('session_key')

        # If the users is new, no session key! Create one1
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}


        # cart is available in all pages
        self.cart = cart 
   
    def db_add(self,product,quantity):
        product_id = str(product)
        product_qty = str(quantity)
 
        # Logic
        if product_id in self.cart:
            pass
        else:
            #self.cart[product_id] = {'price' : str(product.price)}
            self.cart[product_id] = int(product_qty)       

        self.session.modified = True

        # Deal with logged in user
        if self.request.user.is_authenticated:
            # Get the current user profile

            current_user = Profile.objects.filter(user__id= self.request.user.id)
            # Convert {'3':1, '2':4}
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
			# Save carty to the Profile Model
            current_user.update(old_cart=str(carty))

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

        # Deal with logged in user
        if self.request.user.is_authenticated:
            # Get the current user profile

            current_user = Profile.objects.filter(user__id= self.request.user.id)
             # Convert {'3':1, '2':4}
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
			# Save carty to the Profile Model
            current_user.update(old_cart=str(carty))

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

       
      
        if self.request.user.is_authenticated:
            # Get the current user profile

            current_user = Profile.objects.filter(user__id= self.request.user.id)
             # Convert {'3':1, '2':4}
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
			# Save carty to the Profile Model
            current_user.update(old_cart=str(carty))

        thing = self.cart    

        return thing
    

    def delete(self,product):
        product_id = str(product)

        # Delete From dictionary/cart
        if product_id in self.cart:
            del self.cart[product_id]


        self.session.modified = True 

        if self.request.user.is_authenticated:
            # Get the current user profile

            current_user = Profile.objects.filter(user__id= self.request.user.id)
             # Convert {'3':1, '2':4}
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
			# Save carty to the Profile Model
            current_user.update(old_cart=str(carty))

