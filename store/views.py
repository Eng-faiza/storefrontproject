#log way 
# from django.shortcuts import render
# from django.http import HttpResponse

# Create your views here.
# def product_list(request):
#     return HttpResponse("ok")

#easy ways
# from django.shortcuts import render, get_list_or_404
# from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Product, Collection, Review,Cart,cartItem,Customer,ProductImage
from .serializers import ProductSerializer , CollectionSerializer,ReviewSerializer, CartSerializer,CartItemSerializer,AddCartItemSerializer,UpdateCartItemSerializer,CustomerSerializer,ProductImageSerializer
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action 
from rest_framework.filters import SearchFilter,OrderingFilter
from rest_framework.pagination import PageNumberPagination
from .filters import ProductFilter
from rest_framework.mixins import CreateModelMixin
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.views import APIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from rest_framework.mixins import CreateModelMixin,RetrieveModelMixin,DestroyModelMixin, UpdateModelMixin
from rest_framework.permissions import AllowAny, IsAuthenticated,IsAdminUser,DjangoModelPermissions
from .permissions import IsAdminOrReadOnly,FullDjangoPermissions,ViewCustomerHistoryPermissions

@api_view()
def product_list(request):
    # queryset=Product.objects.all()
    queryset=Product.objects.select_related('Collection').all()
    serializer =ProductSerializer(queryset, many=True, context={'request':request})
    return Response(serializer.data)


# desrializing object

@api_view(['GET','POST'])
def product_list(request):
    if request.method=='GET':
    # queryset=Product.objects.all()
    
        queryset=Product.objects.select_related('Collection').all()
        serializer =ProductSerializer(queryset, many=True, context={'request':request})
        return Response(serializer.data)
    elif request.method=='POST':
        serializer=ProductSerializer(data=request.data)


        # if serializer.is_valid():
        #     serializer.validated_data
        #     return Response("ok, saved")
        # else:
        #   return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
     
     # in concise way without top if , else statements 
        serializer.is_valid(raise_exception=True)
        # serializer.validated_data # nb 
        # print(serializer.validated_data) #nb 
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response

#product detail
# @api_view()
# def product_detail(request,id):
#     try:
#         product =Product.objects.get(pk=id)
#         serializer=ProductSerializer(product)
#         return Response(serializer.data)
#     except Product.DoesNotExist:
#         return Response(status=404)

# other way 
@api_view(['GET','PUT', 'DELETE'])
def product_detail(request,id):
   product = get_object_or_404(Product, pk=id)
   if request.method=='GET':
        serializer=ProductSerializer(product)
        return Response(serializer.data)
   elif request.method == 'PUT':
       serializer= ProductSerializer(product, data=request.data)
       serializer.is_valid(raise_exception=True)
       serializer.save()
       return Response(serializer.data)
   elif request.method=='DELETE':
       if product.orderitems.count()>0:
           return Response({'error':"product cann't be deleted because it associated with order item "},status=status.HTTP_405_METHOD_NOT_ALLOWED)
       product.delete()
       return Response(status=status.HTTP_204_NO_CONTENT)
   


# retriving all colections as  list  : with out using class based views 
# @api_view()
# def collection_list(request):
#     queryset=Collection.objects.all()
#     serializer =CollectionSerializer(queryset, many=True, context={'request':request})
#     return Response(serializer.data)

# collection detail  without using class based view
# @api_view(['GET','PUT','DELETE'])
# def collection_detail(request,id):
#     collection= get_object_or_404(Collection,pk=id)
#     if request.method=='GET':
#         serializer=CollectionSerializer(collection)
#         return Response(serializer.data)

#     elif request.method == 'PUT':
#            serializer= CollectionSerializer(collection, data=request.data)
#            serializer.is_valid(raise_exception=True)
#            serializer.save()
#            return Response({
#               'message': 'Collection updated successfully',
#               'data': serializer.data
#                 })  
#     elif request.method=='DELETE':
#            collection.delete()
#            return Response("the colection has deleted successfully ")
       
    

    # try:
    #     product =Product.objects.get(pk=id)
    #     serializer=ProductSerializer(product)
    #     return Response(serializer.data)
    # except Product.DoesNotExist:
    #     return Response(status=404)
   


#  class-based view 

# class CollectionList(APIView):
#     def get(self,request ):
#          queryset=Collection.objects.all()
#          serializer =CollectionSerializer(queryset, many=True, context={'request':request})
#          return Response(serializer.data)
#     def post(self,request):
#          serializer= CollectionSerializer(data=request.data)
#          serializer.is_valid(raise_exception=True)
#          serializer.save()
#          return Response({
#         'message': 'Collection created successfully',
#         'data': serializer.data
#          })  
     

# collection detail  using class-based view 
# class CollectionDetail(APIView):
#     def get(self,request,id ):
#          collection= get_object_or_404(Collection,pk=id)
#          serializer=CollectionSerializer(collection)
#          return Response(serializer.data)

#     def put(self,request,id):
#             collection= get_object_or_404(Collection,pk=id)
#             serializer= CollectionSerializer(collection, data=request.data)
#             serializer.is_valid(raise_exception=True)
#             serializer.save()
#             return Response({
#               'message': 'Collection updated successfully',
#               'data': serializer.data
#                 })  
#     def delete(self,request,id):
#             collection= get_object_or_404(Collection,pk=id)
#             collection.delete()
#             return Response("the colection has deleted successfully ")


# generic views:  concising view creation function 
# class CollectionList(ListCreateAPIView):
#     queryset=Collection.objects.all()
#     serializer_class=CollectionSerializer
#     def get_serializer_context(self):
#          return {'questy': self.request}



# generic views:  concising view get, update, delede functions 

# class CollectionDetail(RetrieveUpdateDestroyAPIView):
    
    # queryset=Collection.objects.all()
    # serializer_class=CollectionSerializer
    # lookup_field='id' #helpes to get your data by not changing your id argument otherwise you need to change id into pk 
  
    # def delete(self,request,id):
    #         collection= get_object_or_404(Collection,pk=id)
    #         collection.delete()
    #         return Response("the colection has deleted successfully ")


# other easy way of generic that makes all GET, PUT, update,PATCH,DELETE: destroy
class CollectionDetail(RetrieveUpdateDestroyAPIView):
    queryset=Collection.objects.all()
    serializer_class=CollectionSerializer
    lookup_field='id'




# view set : collecting mutliple view functions in signle class 
# it allows to use collection_lists, get , put, post and- delete in one class

class CollectionViewSet(ModelViewSet):
    queryset=Collection.objects.all()
    serializer_class=CollectionSerializer
    lookup_field='id'
    permission_classes=[IsAdminOrReadOnly]

    #  these code below you can use if you need or you can leave if you don't have conditio not important 
   
    # def get_serializer_context(self):
    #      return {'request': self.request}
    # def delete(self,request,id):
    #         collection= get_object_or_404(Collection,pk=id)
    #         collection.delete()
    #         return Response("the colection has deleted successfully ")


# distroy logic 
# def destroy(self,request,*args,**kwargs):
#     if orderItem.object.filter(product_id=kwargs['id']).count()>0:
#        return Response({'error':'collection can not be deleted'})
#     return super().destroy(request,*args,**kwargs)



# product view set  with out search but filter
# class ProductViewSet(ModelViewSet):
#     queryset=Product.objects.all()
#     serializer_class=ProductSerializer
#     lookup_field='id'
#     filter_backends=[DjangoFilterBackend]
#     filterset_class=ProductFilter

# searching
class ProductViewSet(ModelViewSet):
         queryset=Product.objects.all()
         serializer_class = ProductSerializer
         filter_backends=[DjangoFilterBackend,SearchFilter]
         filterset_class=ProductFilter
         search_fields=['title','describtion']

#sorting
class ProductViewSet(ModelViewSet):
         queryset=Product.objects.all()
         serializer_class = ProductSerializer
         filter_backends=[DjangoFilterBackend,SearchFilter,OrderingFilter]
         filterset_class=ProductFilter
         search_fields=['title','describtion']
         ordering_fields=['unit_price','last_update']

#pagination
class ProductViewSet(ModelViewSet):
         queryset=Product.objects.prefetch_related('images').all()  #prefetch_related hepls you the image duplicates   
         serializer_class = ProductSerializer
         filter_backends=[DjangoFilterBackend,SearchFilter,OrderingFilter]
         filterset_class=ProductFilter
         pagination_class=PageNumberPagination # if you need delete it's not important since you make pagination default
         permission_classes=[IsAdminOrReadOnly]
         search_fields=['title','describtion']
         ordering_fields=['unit_price','last_update']

# review
class ReviewSet(ModelViewSet):
    queryset=Review.objects.all()
    serializer_class=ReviewSerializer
    
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(
            Product_id=self.kwargs['product_id']
        )
    # if you don't want to use product column 
    def get_serializer_context(self):
      return {
        'product_id': self.kwargs['product_id']
    }


    # #filtering
    # class ProductViewSet(ModelViewSet):
    #  serializer_class = ReviewSerializer

    #  def get_queryset(self):
    #     queryset=Product.objects.all()
    #     collection_id=self.request.query_params.get('collection_id')
    #     if collection_id is not None:
    #         queryset=queryset.filter(collection_id=collection_id)
    #     return queryset
    #     # if you don't want to use product column 
    # def get_serializer_context(self):
    #      return {
    #         'product_id': self.kwargs['product_id']
    #     }


# generic filtering
    # class ProductViewSet(ModelViewSet):
    #  queryset=Product.objects.all()
    #  serializer_class = ProductSerializer
    #  filter_backends=[DjangoFilterBackend]
    # #  filterset_fields=['Collection_id', 'unit-price']
    # filterset_class=ProductFilter
    #     # if you don't want to use product column 
    # def get_serializer_context(self):
    #      return {
    #         'product_id': self.kwargs['product_id']
    #     }




# cart
class CartViewSet(CreateModelMixin, GenericViewSet,DestroyModelMixin, RetrieveModelMixin):
        #  queryset=Cart.objects.all()
        #  queryset=Cart.objects.select_related() for foriegn
         queryset=Cart.objects.prefetch_related('items__product').all() # helps retriving or getting queries
         serializer_class=CartSerializer


class CartItemViewSet(ModelViewSet):
     http_method_names=['get','post', 'delete','patch']
     serializer_class=CartItemSerializer
     def get_serializer_class(self):
          if self.request.method=='POST':
               return AddCartItemSerializer
          elif self.request.method=='PATCH':
               return UpdateCartItemSerializer
          return CartItemSerializer

     def get_serializer_context(self):
          return {'cart_id':self.kwargs['cart_pk']}

     
     def get_queryset(self):
          return cartItem.objects\
            .filter(cart_id=self.kwargs['cart_pk'])\
                .select_related('product')




# user profile 
# class CustomerViewSet(CreateModelMixin, RetrieveModelMixin,UpdateModelMixin,GenericViewSet):
class CustomerViewSet(ModelViewSet):
     queryset=Customer.objects.all()
     serializer_class=CustomerSerializer
    #  permission_classes=[IsAuthenticated]
     permission_classes=[IsAdminUser] # since we don't need too much complexity
    #  permission_classes=[DjangoModelPermissions]
    #  permission_classes=[FullDjangoPermissions]

    # if you need anyone retrieve customer information but only admins or autherized users can updated customers 
    #  def get_permissions(self):
    #       if self.request.method=='GET':
    #        return [AllowAny()]
    #       return[IsAuthenticated()]

     @action(detail=True,permission_classes=[ViewCustomerHistoryPermissions])
     def history(self,request,pk):
      return Response('ok')

# getting profile
     @action(detail=False, methods=['GET','PUT'],permission_classes=[IsAuthenticated])
     def me(self,request):
      (customer,created)=Customer.objects.get_or_create(user_id=request.user.id)
      if request.method=='GET':
       serializer=CustomerSerializer(customer)
       return Response(serializer.data)
      elif request.method=='PUT':
           serializer=CustomerSerializer(customer, data=request.data)
           serializer.is_valid(raise_exception=True)
           serializer.save()
           return Response(serializer.data)
      


# product image 
class ProductImageViewSet(ModelViewSet):
     serializer_class=ProductImageSerializer

     def get_serializer_context(self):
          product_pk = self.kwargs.get('product_pk')
          return {
               'product_id': product_pk,
               'product_pk': product_pk,
          }
     
     def  get_queryset(self):
        return ProductImage.objects.filter(product_id=self.kwargs['product_pk'])
    