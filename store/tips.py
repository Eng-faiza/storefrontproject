#preload realated objects
from store.models import Product


products=Product.objects.select_related('...') 
products=Product.objects.prefetch_related('...') 

#load only what you need 
products=Product.objects.only('title')
products=Product.objects.defer('description')


#use values 
products=Product.objects.values()   
products=Product.objects.values_list()   


#count property
products=Product.objects.count()
len(Product.objects.all()) # not good because it loads all the objects into memory and then counts them

#bulk create/update : if you want to create and update multiple objects at once
Product.objects.bulk_create([])
# Product.objects.bulk_update([], []) # 

