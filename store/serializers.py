from rest_framework import serializers
from decimal import Decimal
from store.models import Product, Collection,Review, Cart, cartItem, Customer, ProductImage

# if you need to container nasted object in your product use this class 

# class CollectionSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     title=serializers.CharField(max_length=255)
   
    # other way 
class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model =Collection
        # fields=['id', 'title','Product_count']
        fields=['id', 'title']

    # Product_count=serializers.IntegerField(read_only=True)


# product image serializer
class ProductImageSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        product_id = self.context.get('product_id') or self.context.get('product_pk')
        if product_id is None:
            raise serializers.ValidationError('Product id is required to create an image.')
        return ProductImage.objects.create(product_id=product_id, **validated_data)

    class Meta:
        model = ProductImage
        fields = ['id', 'image']


# class ProductSerializer(serializers.Serializer):
class ProductSerializer(serializers.ModelSerializer): # ModelSerializer
    images=ProductImageSerializer(many=True, read_only=True)
    class Meta:
        model =Product
        # fields=['__all__'] # if you need to retrieve all your fields but not good 
        fields=['id', 'title','describtion','slug', 'inventory', 'unit_price','price_with_tax', 'Collection','images']
    
    price_with_tax=serializers.SerializerMethodField(method_name='calculate_tax')
           

    # id = serializers.IntegerField()
    # title=serializers.CharField(max_length=255)
    # price=serializers.DecimalField(max_digits=6, decimal_places=2, source='unit_price') #source : to rename your product column name  
    # price_with_tax=serializers.SerializerMethodField(method_name='calculate_tax')
    # # display data as int
    # collection = serializers.PrimaryKeyRelatedField(
    #     queryset=Collection.objects.all() # display data as int
    # )
     #representing collections as string 
    # Collection=serializers.StringRelatedField()
    #nasted object
    # Collection=CollectionSerializer()
    #hyperlink related field 
    # Collection=serializers.HyperlinkedRelatedField(
    #     queryset=Collection.objects.all(),
    #     view_name='collection_detail'
    # )



    def calculate_tax(self, product:Product):
        return product.unit_price* Decimal(1.1)




    # overwriting the product creation 
    # def create(self, validated_data):
    #     product=Product(**validate_data)
    #     product.other=1
    #     product.save()
    #     return product

    # # overwriting the product creation . instance : project object
    # def update(self, instance, validated_data):
    #     instance.unit_price=validated_data.get('unit_price')
    #     instance.save()
    #     return instance
  


  # review serializer
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model= Review
        fields=['id','date','name','description','Product' ]


# if you don't want to use product column
    # def create(self,validated_data):
    #     product_id=self.context['product_id']
    #     return Review.objects.create(product_id=product_id,**validated_data)




# product information if you don't need to use the entire product ibject 

class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields=['id','title','unit_price']

# cartItem
class CartItemSerializer(serializers.ModelSerializer):
    # product=ProductSerializer() #if you need to retrive the entire product information
    product=SimpleProductSerializer()
    total_price=serializers.SerializerMethodField()
    def get_total_price(self,cart_item:cartItem):
        return cart_item.quantity*cart_item.product.unit_price
    class Meta:
        model=cartItem
        fields=['id','product','quantity','total_price']


#cart serializers
class CartSerializer(serializers.ModelSerializer):
    id=serializers.UUIDField(read_only=True)
    items=CartItemSerializer(many=True,read_only=True)
    total_price=serializers.SerializerMethodField()
    def get_total_price(self,cart):
         return sum([item.quantity*item.product.unit_price for item in cart.items.all()])
          
    class Meta:
        model=Cart
        fields=['id','items','total_price']


class AddCartItemSerializer(serializers.ModelSerializer):
    product_id=serializers.IntegerField()

    # invalid error validation
    def validate_product_id(self,value):
        if not Product.objects.filter(pk=value).exists():
            raise serializers.ValidationError('no product with the given id ')
        return value

    def save (self,**kwargs):
        cart_id= self.context['cart_id']
        product_id = self.validated_data['product_id']
        quantity = self.validated_data['quantity']

        try :
         cart_item = cartItem.objects.get(cart_id=cart_id,product_id=product_id)
            # updating an existing item 
         cart_item.quantity+=quantity
         cart_item.save()
         self.instance=cart_item
        except cartItem.DoesNotExist:
            #creating new item 
            self.instance=cartItem.objects.create(cart_id=cart_id, **self.validated_data)
        return self.instance

    class Meta:
        model=cartItem
        fields=['id','product_id','quantity']



class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model=cartItem
        fields=['quantity']


# building user profile 
class CustomerSerializer(serializers.ModelSerializer):
    user_id=serializers.IntegerField(read_only=True)
    class Meta: 
        model=Customer
        fields=['id','user_id', 'phone', 'birth_date','membership']





