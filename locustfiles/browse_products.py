from locust import HttpUser, task, between
from random import randint

class website_user(HttpUser):
    waite_time=between(1,5)
    @task(2)
    def view_products(self):
        # print('viewing products')
        collection_id=randint(2,6)
        self.client.get(f"/store/products/?collection_id={collection_id}/", name="/store/products/")  # using name to group the requests in the report

    @task(4)
    def view_products(self):
        # print('view products')
        product_id=randint(1,1000)
        self.client.get(f"/store/products/{product_id}/", name="/store/products/:id")  # using name to group the requests in the report

    @task(1)
    def add_to_cart(self):
        # print('adding to cart')
        product_id=randint(1,10)
        self.client.post(f"/store/carts/{self.cart_id}/items/",
        name="/store/carts/items",
        json={"product_id": product_id, "quantity": 1})  # using name to group the requests in the report

    @task
    def say_hello(self):
        self.client.get("/playground/hello/", name="/playground/hello")  # using name to group the requests in the report

    def on_start(self):
        response = self.client.post("/store/carts/")
        result = response.json()
        self.cart_id = result["id"]