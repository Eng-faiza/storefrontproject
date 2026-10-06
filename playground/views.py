from django.shortcuts import render
from django.http import HttpResponse, request
from store import models
from store.models import Order, Product, OrderItem, Customer, Collection, Promotion
from django.db.models import Q, F, DecimalField ,Func , ExpressionWrapper
from django.db.models.aggregates import Count, Min, Max, Avg, Sum
from django.db.models import Value
from django.db.models.functions import Concat
from django.contrib.contenttypes.models import ContentType
from django.db import connection, transaction


import requests
#sending emails 
# from django.core.mail import  EmailMessage, send_mail, mail_admins, BadHeaderError
# from templated_mail.mail import BaseEmailMessage

#celery 
from .tasks import notify_customers
# cache
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from rest_framework.views import APIView
from  django.utils.decorators import method_decorator


# logging 
import logging

def say_hello(request):
    queryset=Product.objects.all()
    # queryset=Product.objects.count()
    # queryset=queryset.filter().filter().order_by()
    # for product in queryset:
    #     print(product)
    # product =Product.objects.get(pk=1)
    # product_exists =Product.objects.filter(pk=0).exists()


    queryset =Product.objects.filter(unit_price__range=(20, 30))
    # queryset =Product.objects.filter(collection_id__range=(1, 2,3))
    queryset =Product.objects.filter(title__icontains='coffee')
    queryset =Product.objects.filter(title__startswith='coffee')
    queryset =Product.objects.filter(last_update__year=2021)
    queryset =Product.objects.filter(last_update__year=2021)

    # filtering using Q objects
    queryset =Product.objects.filter(Q(inventory__lt=10) | Q(unit_price__lt=20))
    queryset =Product.objects.filter(Q(inventory__lt=10) & Q(unit_price__lt=20))
    queryset =Product.objects.filter(Q(inventory__lt=10) & ~ Q(unit_price__lt=20)) # inventory less than 10 and unit price not less than 20

    # referencing fields using F objects
    queryset =Product.objects.filter(inventory=F('unit_price')) # inventory equal to unit price

    # sorting 
    queryset = Product.objects.order_by('title') # ascending
    queryset = Product.objects.order_by('-title') # descending use (-) if you wanna change the direction of your object ording 
    queryset = Product.objects.order_by('unit_price', '-title').reverse() # reverse the order of the queryset 
    product = Product.objects.order_by('unit_price')[0] # returns query set 
    product = Product.objects.earliest('unit_price') # returns the first object in the queryset based on the unit price


    # limiting the number of results returned
    queryset = Product.objects.all()[:5] # returns the first 5 objects in the queryset
    queryset = Product.objects.values('id','title')
    queryset = Product.objects.values('id','title', 'Collection__title') # returns a list of dictionaries with the specified fields


    #order items
    # queryset = OrderItem.objects.values('Product_id')# returns a list of order items with the related product object and makes duplicates 
    # queryset = OrderItem.objects.values('Product_id').distinct() # returns a list of order items with the related product object . doesn't display any diplicates
    # Product.objects.filter(id__in=OrderItem.objects.values('Product_id').distinct()) # returns a list of products that have been ordered and doesn't display any duplicates
    
    # result = Product.objects.aggregate(count=Count('id'), min_price=Min('unit_price'), max_price=Max('unit_price')) # returns the total number of products in the database
    # result = Product.objects.filter(Collection_id=1).aggregate(count=Count('id'), min_price=Min('unit_price'), max_price=Max('unit_price')) # returns the total number of products in the database

    queryset = Customer.objects.annotate(is_new=Value(True))
    queryset = Customer.objects.annotate(new_id=F('id'))
    queryset = Customer.objects.annotate(new_id=F('id')+1)
    queryset = Customer.objects.annotate(
        #concat
        full_name=Func(F('first_name'),Value(' '), F('last_name'), function='CONCAT')
    )
    # easy way 
    queryset = Customer.objects.annotate(
        full_name=Concat('first_name', Value(' '), 'last_name')
    )

    #grouping data 
    queryset = Customer.objects.annotate(
        orders_count=Count('order')
    )

    #ExpressionWrapper
    discounted_price = ExpressionWrapper(F('unit_price') * 0.8, output_field=DecimalField())
    queryset = Product.objects.annotate(
        discounted_price=discounted_price
    )

    # query generic relationships

    #custom managers
    # TaggedItem.objects.get_tags_for(Product, 1)



    #understanding queryset catch
    queryset = Product.objects.all()
    list(queryset) # hits the database
    list(queryset) # doesn't hit the database because the queryset is cached
    queryset[0]
    list(queryset) 

    #creating objects
    collection = Collection()
    collection.title = 'Video Games'
    collection.featured_product = Product(pk=1)
    # collection.featured_product_id = 1
    collection.save()
    collection.id

    #short way 
    # collection.objects.create(title='Video Games', featured_product_id=1)


    # updating objects
    # collection = Collection(pk=11) # gives title column empty strig
    # collection = Collection.objects.get(pk=11) #
    # # collection.title = 'Games'
    # collection.featured_product = None
    # collection.save()

    # other way
    # collection.objects.update(featured_product=None) # updates all the objects in the collection table and sets the featured_product to None
    # collection.objects.filter(pk=11).update(featured_product=None) # updates  the id=11 objects  in the collection table and sets the featured_product to None


    # deleting objects
    # collection = Collection(pk=11)
    # collection.delete() # deletes specific object from the database``

    #deleting multiple objects
    # Collection.objects.filter(id__gt=5).delete() # deletes all the objects with id greater than 5


    #transaction nd: we create parent record before child record because of foreign key constraint
    
    
    with transaction.atomic(): 
        order = Order()
        order.Customer_id = 1
        order.save()

        item = OrderItem()
        item.Order = order
        item.Product_id = 1
        item.quantity = 1
        item.unit_price = 10
        item.save()


    # executing raw sql queries
    queryset = Product.objects.raw('SELECT * FROM store_product')
    queryset = Product.objects.raw('SELECT id, title FROM store_product')

    # other way
    # cursor = connection.cursor() # returns a cursor object that can be used to execute raw sql queries
    # cursor.execute('SELECT * FROM store_product') #we can write every sql statement , selec , insert ans so on 
    # cursor.close() # closes the cursor object and releases the database connection back to the connection pool
    # other  way 
    # with connection.cursor() as cursor:
    #     cursor.execute('') # first way of excuting store queries
    #     cursor.callproc('get_customers',[1,3, 'John' ]) # second way 

    #     cursor.fetchall() # returns a list of tuples with the results of the query
    # return render(request, 'hello.html',{'name':'faiza', 'result':list(queryset)})
    
    
    
    # return render(request, 'hello.html',{'name':'faiza', 'result':result})

    return render(request, 'hello.html',{'name':'faiza', 'products':list(queryset)})
    return render(request, 'hello.html',{'name':'faiza', 'product':product})
    return render(request, 'hello.html',{'name':'faiza', 'products':list(queryset)})
  
    



#sending emails

# def greetings(request):
    # try:
    #  send_mail('subject', 'message','info@faizamahdi.com',['ds@faiza.com'])
    #  mail_admins('subject', 'message',html_message='message')
      
    #   sending file email
    #    message=EmailMessage('subject','message', 'from@faizamahdi.com',['ali@faizabuy.com'])
    #    message.attach_file('playground/static/images/girl.jpg')
    #    message.send()

     # email templates

    #     message=BaseEmailMessage(
    #         template_name='emails/hello.html',
    #         context={'name':'faiza'}
    #     )
    #     message.send(['john@faizabuy.com'])

    # except BadHeaderError:
    #    pass
    # return render (request, 'hello.html',{'name':'faiza'})


#celery
# def greetings(request):
#     notify_customers.delay("hello")# message you wanna send 
#     return render(request, 'hello.html',{'name':'faiza'})
     

# catching : simulating a slow request to test the performance of the application
# def greetings(request):
#      key = 'httpbin_result'
#      if cache.get(key) is None:
#         response = requests.get('https://httpbin.org/delay/2') # this will take 2 seconds to respond
#         data=response.json()
#         cache.set(key, data,) # cache the result for 30 seconds
#      return render(request, 'hello.html',{'name':cache.get(key)})
     

# catch page decorator : caching the result of the view for 5 minutes 
# @cache_page(5*60) 
# def greetings(request):
#      key = 'httpbin_result'
#      if cache.get(key) is None:
#         response = requests.get('https://httpbin.org/delay/2') # this will take 2 seconds to respond
#         data=response.json()
#      return render(request, 'hello.html',{'name':data})
    

# CLASS BASED VIEWS
class HelloView(APIView):
    def get(self, request):
        return render(request, 'hello.html',{'name':'faiza'})


#other way of example  class based views
# class HelloView(APIView):
#     def get(self, request):
#         response = requests.get('https://httpbin.org/delay/2') # this will take 2 seconds to respond
#         data=response.json()
#         return render(request, 'hello.html',{'name':data})



# logging
logger = logging.getLogger(__name__)



# other way of example  class based views
class HelloView(APIView):
    @method_decorator(cache_page(5*60)) # caching the result of the view for 5 minutes
    def get(self, request):
        try:
            logger.info("calling httpbin")
            response = requests.get('https://httpbin.org/delay/2') # this will take 2 seconds to respond
            logger.info("recieving response ")
            data=response.json()
        except requests.connectionError:
            logger.critical("httpbin is offline")
        return render(request, 'hello.html',{'name':data})


