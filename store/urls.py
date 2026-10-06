from django.urls import path 
# from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from .import views
# from pprint import pprint



# routers : nb these bellow three lines use only when you're using : ModelViewSet
# router=SimpleRouter() # nb if you use instead of simpleRouter > default you get the urls you have in your project


#use in  nasted routers  
router=routers.DefaultRouter() #parent router

router.register('collections',views.CollectionViewSet)
router.register('products',views.ProductViewSet, basename='products') # you'll need this basename when you use filtering other wise it doesnot work 
router.register('carts',views.CartViewSet)
router.register('customers',views.CustomerViewSet)
# pprint(router.urls) # allows to print your urls in terminal 

products_router=routers.NestedDefaultRouter(router,'products',lookup='product') #child router
products_router.register('reviews',views.ReviewSet,basename='product-reviews')
products_router.register('images',views.ProductImageViewSet,basename='product_images')

#nasted routers
carts_router=routers.NestedDefaultRouter(router,'carts',lookup='cart')
carts_router.register('items',views.CartItemViewSet,basename='cart-items-detail')

# url configration and normal routs if you don't use ModelViewSet
# urlpatterns = [
#      path('products/', views.product_list),
#      # path('collections/', views.collection_list),  normal api view 
#      path('collections/', views.CollectionList.as_view()), #class-based view , as_view(): converts the class regular based view 
#      path('products/<int:id>/', views.product_detail), # int: hepls you to search your products only numbers if you don't want that you can leave it 
#      # path('collections/<int:id>/', views.collection_detail, name='collection_detail')
#      path('collections/<int:id>/', views.CollectionDetail.as_view(), name='CollectionDetail')

# ]


# ModelViewSet and  routers

# urlpatterns = [
#     path('', include(router.urls)),
# #     you can put here the other urls you need if you have 

# ] 

# or 
urlpatterns=router.urls + products_router.urls+carts_router.urls


