from locust import HttpUser, task, between

class DummyJsonUser(HttpUser):
    wait_time = between(1, 3)
    host = "https://dummyjson.com"

    @task
    def get_users(self):
        self.client.get("/users/1")


    @task
    def update_user(self):
        payload = {
            "firstName": "Jane",
            "lastName": "Smith"
        }
        self.client.put("/users/1", json=payload)

    @task
    def delete_user(self):
        self.client.delete("/users/1")

    @task
    def get_products(self):
        self.client.get("/products/1")


class FakeStoreApiUser(HttpUser):
    wait_time = between(1, 3)
    host = "https://fakestoreapi.com"

    @task
    def get_products(self):
        self.client.get("/products/1")

    @task
    def create_product(self):
        payload = {
            "title": "Test Product",
            "price": 10.99,
            "description": "A test product",
            "image": "https://i.pravatar.cc",
            "category": "electronics"
        }
        self.client.post("/products", json=payload)

    @task
    def update_product(self):
        payload = {
            "title": "Updated Product",
            "price": 12.99
        }
        self.client.put("/products/1", json=payload)

    @task
    def delete_product(self):
        self.client.delete("/products/1")

    @task
    def get_users(self):
        self.client.get("/users/1")

    @task
    def update_user(self):
        payload = {"username": "john_updated"}
        self.client.put("/users/1", json=payload)

    @task
    def delete_user(self):
        self.client.delete("/users/1")

class FakeApiNetUser(HttpUser):
    host = "https://fakeapi.net"
    wait_time = between(1, 3)

    @task
    def get_products(self):
        self.client.get("/products/1")


   