from django.contrib import admin 
from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator, FileExtensionValidator
from uuid import uuid4
from store.validators import validate_file_size


class Promotion(models.Model):
    discription=models.CharField(max_length=255)
    discount=models.FloatField()


class Collection(models.Model):
    title=models.CharField(max_length=255)
    featured_product=models.ForeignKey('Product',on_delete=models.SET_NULL,null=True, related_name='+')

    # overwritting object into sting 
    def __str__(self)->str:
        return self.title

    # default ordering of the collection model
    class Meta:
        ordering=['title']

class Product(models.Model):
    title=models.CharField(max_length=255)
    slug=models.SlugField()
    describtion=models.TextField(null=True, blank=True) # null=True allows the field to be empty in the database, blank=True allows the field to be empty in forms
    unit_price=models.DecimalField(max_digits=6,decimal_places=2, validators=[MinValueValidator(1)]) # max_digits is the total number of digits, decimal_places is the number of digits after the decimal point
    inventory=models.IntegerField()
    last_update=models.DateTimeField(auto_now=True)
    Collection=models.ForeignKey(Collection,on_delete=models.PROTECT)
    promotions=models.ManyToManyField(Promotion, blank=True)

    def __str__(self)->str:
            return self.title
    # default ordering of the collection model
    class Meta:
            ordering=['title']


#media images  

class ProductImage(models.Model):
     product=models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
     image=models.ImageField(
          upload_to='store/images',
          validators=[validate_file_size])
    
    #  file validation
    #  image=models.FileField(
    #       upload_to='store/images',
    #       validators=[FileExtensionValidator(allowed_extensions=['pdf'])])  #it entends only the package file validation error 



class Customer(models.Model):
    MEMBERSHIP_BRONZE='B'
    MEMBERSHIP_SILVER='S'
    MEMBERSHIP_GOLD='G'
    MEMBERSHIP_CHOICES=[
        (MEMBERSHIP_BRONZE, 'Bronze'),
        (MEMBERSHIP_SILVER, 'Silver'),
        (MEMBERSHIP_GOLD, 'Gold'),
    ]
    phone=models.CharField(max_length=255)
    birth_date=models.DateField(null=True)
    membership=models.CharField(max_length=1 , choices=MEMBERSHIP_CHOICES,default=MEMBERSHIP_BRONZE)
    user=models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # def __str__(self):
    #         return f'{self.first_name}{self.last_name}'
    # class Meta:
    #         ordering=['first_name','last_name']

    def __str__(self):
            return f'{self.user.first_name}{self.user.last_name}'

    @admin.display(ordering='user__first_name')
    def first_name(self):
         return self.user.last_name
    @admin.display(ordering='user__last_name')
    def last_name(self):
         return self.user.last_name
    

    class Meta:
            ordering=['user__first_name','user__last_name']
            permissions=[
                 ('view_history','Can view history')
            ]

    # class Meta:
    #     db_table='store_customers' changes table name 
    #     indexes=[
    #         models.Index(fields=['last_name','first_name'])
    #     ]

class Order(models.Model):
    PAYMENT_STATUS_PENDING='P'
    PAYMENT_STATUS_COMPLETED='C'
    PAYMENT_STATUS_FAILED='F'
    PAYMENT_STATUS_CHOICES =[
        (PAYMENT_STATUS_PENDING,'pending'),
        (PAYMENT_STATUS_COMPLETED,'complete'),
        (PAYMENT_STATUS_FAILED,'failed'),
    ]

    placed_at=models.DateTimeField(auto_now_add=True)
    payment_status=models.CharField(max_length=1, choices=PAYMENT_STATUS_CHOICES,default=PAYMENT_STATUS_PENDING)
    Customer=models.ForeignKey(Customer,on_delete=models.PROTECT)


    # creating custom permission
    class Meta:
         permissions=[
              ('cancel_order','Can cancel order')
         ]
     # overwritting object into sting 
    def __str__(self) -> str:
      return f'{self.Customer.first_name} {self.Customer.last_name}'


    
class OrderItem(models.Model):
    Order=models.ForeignKey(Order, on_delete=models.PROTECT)
    Product=models.ForeignKey(Product, on_delete=models.PROTECT, related_name='orderitems')
    quantity=models.PositiveSmallIntegerField()
    unit_price=models.DecimalField(max_digits=6,  decimal_places=2)


class Address(models.Model):
    street=models.CharField(max_length=255)
    city=models.CharField(max_length=255)
    Customer=models.ForeignKey(Customer,on_delete=models.CASCADE)
    zip = models.CharField(max_length=20)

class Cart(models.Model):
    id=models.UUIDField(primary_key=True, default=uuid4)
    created_at=models.DateTimeField(auto_now_add=True)

class cartItem(models.Model):
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE, related_name='items')
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)] # minimum value can be entered 
    )

    class Meta:
        unique_together=[['cart','product']]







# review 

class Review(models.Model):
    Product=models.ForeignKey(Product,on_delete=models.CASCADE, related_name='reviews')
    name = models.CharField(max_length=255)
    description=models.TextField()
    date=models.DateField(auto_now_add=True)
    