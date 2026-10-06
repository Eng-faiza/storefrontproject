
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient  # you don't need if we you use fixture 
import pytest
from store.models import Collection, Product
from model_bakery import baker
from store.test.conftest import api_client

@pytest.fixture
def create_collection(api_client):
 def do_create_collection(collection):
  return api_client.post('/store/collections/',collection )
 return do_create_collection


@pytest.mark.django_db
# class TestCreateCollection:
#  # @pytest.mark.skip # skipping tests 
#  def test_if_user_is_anonymous_returns_401(self):
#   client=APIClient() # delete this line when you using fixtures
#   response=client.post('/store/collections/' , {'title':'a'})
#   assert response.status_code==status.HTTP_401_UNAUTHORIZED

# #  user authentication
#  def test_if_user_is_not_admin_returns_403(self):
#   client=APIClient()
#   client.force_authenticate(user={})  
#   response=client.post('/store/collections/' , {'title':'a'})
#   assert response.status_code==status.HTTP_403_FORBIDDEN

# #  multiple assertions 
#  def test_if_user_is_invalid_returns_400(self):
#   client=APIClient()
#   client.force_authenticate(user={User(is_staff=True)})  
#   response=client.post('/store/collections/' , {'title':''})
#   assert response.status_code==status.HTTP_400_BAD_REQUEST
#   assert response.data['title'] is not None


#  def test_if_user_is_valid_returns_201(self):
#   client=APIClient()
#   client.force_authenticate(user={User(is_staff=True)})  
#   response=client.post('/store/collections/' , {'title':'a'})
#   assert response.status_code==status.HTTP_201_CREATED
#   assert response.data['id'] > 0 


#fixtures : removing duplicates of our code 
class TestCreateCollection:
 # @pytest.mark.skip # skipping tests 
 def test_if_user_is_anonymous_returns_401(self,create_collection):
  response=create_collection( {'title':'a'})
#   response=api_client.post('/store/collections/' ,)
  assert response.status_code==status.HTTP_401_UNAUTHORIZED

#  user authentication
 def test_if_user_is_not_admin_returns_403(self, authenticate,create_collection): 
  authenticate(is_staff=False) # user is not admin
  response=create_collection({'title':'a'})
  assert response.status_code==status.HTTP_403_FORBIDDEN

#  multiple assertions 
 def test_if_data_is_invalid_returns_400(self, authenticate,create_collection):
#   api_client.force_authenticate(user={User(is_staff=True)})  
  authenticate(is_staff=True)
  response=create_collection({'title':''})
  assert response.status_code==status.HTTP_400_BAD_REQUEST
  assert response.data['title'] is not None


 def test_if_data_is_valid_returns_201(self,authenticate,create_collection):
#   api_client.force_authenticate(user={User(is_staff=True)})  
  authenticate(is_staff=True)
  response=create_collection({'title':'a'})
  assert response.status_code==status.HTTP_201_CREATED
  assert response.data['id'] > 0 




# retrieving collections

@pytest.mark.django_db
class TestRetriveCollection:
 def test_if_collection_exists_returns_200(self,api_client):
  collection=baker.make(Collection) # creating collection object
#   baker.make(Product, collection=collection, _quantity=10) # creating 10 product objects for the collection
  response=api_client.get(f'/store/collections/{collection.id}/')
  assert response.status_code==status.HTTP_200_OK
  assert response.data=={
   'id':collection.id,
    'title':collection.title,
    # 'products_count':0
  }



  