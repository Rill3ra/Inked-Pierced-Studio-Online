# cart/cart.py
from decimal import Decimal
from django.conf import settings
from products.models import Product, Certificate
from coupons.models import Coupon

class Cart:
    def __init__(self, request):
        """
        Initialize the cart.
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
        self.coupon_id = self.session.get('coupon_id')

    def add(self, item, quantity=1, override_quantity=False):
        """
        Add a product to the cart or update its quantity.
        """
        item_id = str(item.id)  # Use item.id instead of product.id
        item_type = 'product' if isinstance(item, Product) else 'certificate'
        key = f'{item_type}_{item_id}'

        if key not in self.cart:
            self.cart[key] = {'quantity': 0,
                                  'price': str(item.price),
                                  'type': item_type,
                                  'item_id': item_id}

        if override_quantity:
            self.cart[key]['quantity'] = quantity
        else:
            self.cart[key]['quantity'] += quantity

        self.save()

    def save(self):
        # update the session cart
        self.session[settings.CART_SESSION_ID] = self.cart
        # mark the session as "modified" to be sure it is saved
        self.session.modified = True

    def remove(self, item_id):
        """
        Remove a product from the cart.
        """
        keys_to_remove = []
        for key, item in self.cart.items():
            if item['item_id'] == str(item_id):
                keys_to_remove.append(key)

        for key in keys_to_remove:
            del self.cart[key]
        self.save()

    def __iter__(self):
        """
        Iterate over the items in the cart and get the products from the database.
        """
        cart_copy = self.cart.copy()
        for key, item in cart_copy.items():
            item['price'] = Decimal(item['price'])
            item_type = item['type']
            item_id = item['item_id']

            if item_type == 'product':
                try:
                    item['product'] = Product.objects.get(id=item_id)
                except Product.DoesNotExist:
                    continue
            elif item_type == 'certificate':
                try:
                    item['certificate'] = Certificate.objects.get(id=item_id)
                except Certificate.DoesNotExist:
                    continue

            item['total_price'] = item['price'] * item['quantity']

            # Calculate discount for each item
            if self.coupon:
                discount_rate = self.coupon.discount / Decimal(100)
                item['discount'] = discount_rate * item['total_price']
                item['total_price_after_discount'] = item['total_price'] - item['discount']
            else:
                item['discount'] = Decimal(0)
                item['total_price_after_discount'] = item['total_price']

            yield item

    def __len__(self):
        """
        Count all items in the cart.
        """
        return sum(int(item['quantity']) for item in self.cart.values())

    def get_total_price(self):
        total = Decimal('0.00')
        for item in self:
            total += item['price'] * item['quantity']
        return total

    def clear(self):
        # remove cart from session
        del self.session[settings.CART_SESSION_ID]
        if self.coupon_id:
            del self.session['coupon_id']
        self.session.modified = True

    @property
    def coupon(self):
        if self.coupon_id:
            try:
                return Coupon.objects.get(id=self.coupon_id)
            except Coupon.DoesNotExist:
                return None
        return None

    def get_discount(self):
        if self.coupon:
            return (self.coupon.discount / Decimal(100)) * self.get_total_price()
        return Decimal(0)

    def get_total_price_after_discount(self):
        return self.get_total_price() - self.get_discount()