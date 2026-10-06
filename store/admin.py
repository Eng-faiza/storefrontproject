from django.contrib import admin
from django.db.models import QuerySet
from django.db.models.aggregates import Count
from store import models
from store.models import Collection, Order, OrderItem, Product , Customer, Promotion
#  or  other way 
# from . import models
from  django.utils.html import format_html,urlencode
from django.urls import reverse
# from django.contrib.contenttypes.admin import GenericTabularInline
# from tags.models import TaggedItem

class InventoryFilter(admin.SimpleListFilter):
    title='inventory'
    parameter_name='inventory'

    def lookups(self, request, model_admin):
        return [
            ('<10','Low'),
            
        ]
    def queryset(self, request, queryset: QuerySet):
        if self.value() == '<10':
            return queryset.filter(inventory__lt=10)
       
class ProductImageInline(admin.TabularInline):
    model=models.ProductImage
    readonly_fields=['thumbnail']

    def thumbnail(self,instance):
        if instance.image.name!='':
            return format_html(
            '<img src="{}" class="thumbnail"/>',
            instance.image.url
        )
            # return format_html(f'<img src="{instance.image.url}" class="thumbnail"/>')
        return ''




        
class ProductAdmin(admin.ModelAdmin):
    autocomplete_fields=['Collection'] # to autocomplete the collection field in the admin site
    prepopulated_fields={'slug':['title']} # auto fill the slug field with the title field
    actions=['clear_inventory'] # adding action to the admin site
    # inlines=[TagInLine]
    inlines=[ProductImageInline]
    list_display=['title','unit_price','inventory_status','last_update', 'collection_title'] # list_display to display 
    list_editable=['unit_price',]
    list_filter=['Collection', 'last_update', InventoryFilter] # to filter the products by collection
    list_per_page=10
    ordering=['title']
    search_fields=['title'] # case insensitive search
    prepopulated_fields={'slug':['title']} # auto fill the slug field with the title field
    #selecting related fields to reduce the number of queries to the database
    list_select_related=['Collection'] # to reduce the number of queries to the database

    def collection_title(self, product):
        return product.Collection.title

    @admin.display(ordering='inventory') # ordering the inventory column in the admin site
    #  adding computed column 
    def inventory_status(self, product):
        if product.inventory < 10:
            return 'Low'
        return 'OK'

    @admin.action(description='Clear inventory') # adding action to the admin site
    def clear_inventory(self, request, queryset):
        updated_count=queryset.update(inventory=0)
        self.message_user(
            request,
            f'{updated_count} products were successfully updated.'
        )

    class Media:
        css={
            'all':['store/style.css']
        }

@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display=['title','product_count'] # list_display to display 
    search_fields=['title__istartswith'] # case insensitive search
    list_per_page=10
    ordering=['title']

    @admin.display(ordering='products_count') # ordering the product_count column in the admin site
    def product_count(self,collection):
        url = (
             reverse('admin:store_product_changelist')
        + '?'
        + urlencode({
            'Collection__id': str(collection.id)
        })
        )
        return format_html('<a href="{}">{}</a>', url, collection.products_count)
        
    
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            products_count=Count('product')) # to reduce the number of queries to the database

@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display=['first_name','last_name','membership'] # list_display to display 
    list_editable=['membership']
    list_per_page=10
    list_select_related=['user']
    ordering=['user__first_name', 'user__last_name']
    # search_fields=['first_name__startswith','last_name__startswith'] # case sensitive search
    search_fields=['first_name__istartswith','last_name__istartswith'] # case insensitive search

class OrderItemInline(admin.TabularInline): # TabularInline: to display the order items in row 
# class OrderItemInline(admin.StackedInline): # StackedInline: to display the order items in columns instead of rows 
    model=OrderItem
    autocomplete_fields=['Product'] # in line form to autocomplete the product field
    extra=0 # to remove the extra empty form in the inline form
    min_num=1 # to require at least one inline form
    max_num=10 # to limit the number of inline forms to 10
    model = OrderItem # to display the order items in the order admin page 


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    autocomplete_fields=['Customer']
    inlines=[OrderItemInline]
    list_display=['id','placed_at','Customer'] # list_display to display 
    list_per_page=10
  

# Registering models .

admin.site.register(Product, ProductAdmin)
# admin.site.register(Collection, CollectionAdmin)
admin.site.register(OrderItem)
# admin.site.register(Customer, CustomerAdmin) # ma ubaahnid ina amrkale qortid madama kor kuso shegtey 




#order way of customizing models in the admin site

# @admin.register(models.Product)
# class ProductAdmin(admin.ModelAdmin):
#     list_display=['title','unit_price','inventory','last_update'] # list_display to display 

# admin.site.register(Product)


