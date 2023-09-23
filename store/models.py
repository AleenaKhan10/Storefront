from django.db import models

# Create your models here.
class Promotion(models.Model):
    description = models.CharField(max_length=225)
    discount = models.FloatField()
    
    def __str__(self):
        return self.description

class Collection(models.Model):
    title = models.CharField(max_length=225)
    featured_product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True, blank=True, related_name='+')
    
    def __str__(self):
        return self.title
    
    
class Product(models.Model):
    slug = models.SlugField()
    title = models.CharField(max_length=225)
    description = models.TextField(max_length=225)
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    inventory = models.IntegerField()
    last_updated = models.DateTimeField(auto_now=True)
    collection = models.ForeignKey(Collection, on_delete=models.PROTECT)
    promotion = models.ManyToManyField(Promotion)
    
    def __str__(self):
        return self.title
    
    
class Customer(models.Model):
    MEMBERSHIP_BRONZE = 'B'
    MEMBERSHIP_SILVER = 'S'
    MEMBERSHIP_GOLD = 'G'
    
    MEMBERSHIP_CHOICES = [
        (MEMBERSHIP_BRONZE, 'Bronze'),
        (MEMBERSHIP_SILVER, 'Silver'),
        (MEMBERSHIP_GOLD, 'GOlD'),
    ]
    first_name = models.CharField(max_length=225)
    last_name = models.CharField(max_length=225)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=225)
    birth_date = models.DateField(null=True)
    membership = models.CharField(max_length=1, choices=MEMBERSHIP_CHOICES, default=MEMBERSHIP_BRONZE)
    
    def __str__(self):
        return self.first_name
    
class Order(models.Model):
    PAYMENT_STATUS_PENDING = 'P'
    PAYMENT_STATUS_COMPLETE = 'C'
    PAYMENT_STATUS_FAILED = 'F'
    
    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_STATUS_PENDING, 'Pending'),
        (PAYMENT_STATUS_COMPLETE, 'Complete'),
        (PAYMENT_STATUS_FAILED, 'Failed'),
    ]
    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=1, choices=PAYMENT_STATUS_CHOICES, default=PAYMENT_STATUS_PENDING)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    
    def __str__(self):
        return self.placed_at.strftime('%Y-%m-%d %H:%M:%S')
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantit = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    
    def __str__(self):
        return f'{self.product.title}'
    

class Address(models.Model):
    street = models.CharField(max_length=225)
    city = models.CharField(max_length=225)
    customer = models.ForeignKey(Customer,  on_delete=models.CASCADE)
    
    def __str__(self):
        return self.street
    
class Cart(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.created_at.strftime("%Y-%m-%d %H:%M:%S")
    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()
    
    def __str__(self):
        return f"{self.product.title} - Quantity: {self.quantity}"