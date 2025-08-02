from locust import HttpUser, task, between

class FakeStoreUser(HttpUser):
    wait_time = between(1, 2)

    @task(1)
    def get_products(self):
        self.client.get("/products")

    @task(2)
    def get_product(self):
        self.client.get("/products/1")

    @task(1)
    def get_users(self):
        self.client.get("/users")

    @task(2)
    def get_user(self):
        self.client.get("/users/1")

    @task(1)
    def create_user(self):
        headers = {"Content-Type": "application/json"}
        payload = {
            "id": 11,
            "username": "john_doe",
            "email": "johndoe@example.com",
            "password": "password123",
            "name": {
                "firstname": "John",
                "lastname": "Doe"
            },
            "address": {
                "city": "New York",
                "street": "123 Street",
                "number": 123,
                "zipcode": "10001",
                "geolocation": {
                    "lat": "40.7173",
                    "long": "74.0060"
                }
            },
            "phone": "123-456-7890"
        }
        self.client.post("/users", headers=headers, json=payload)

    @task(1)
    def update_user(self):
        headers = {"Content-Type": "application/json"}
        payload = {
            "name": {
                "firstname": "Jane",
                "lastname": "Doe"
            },
            "address": {
                "city": "New York",
                "street": "123 Street",
                "number": 123,
                "zipcode": "10001",
                "geolocation": {
                    "lat": "40.7173",
                    "long": "74.0060"
                }
            }
        }
        self.client.put("/users/1", headers=headers, json=payload)

    @task(1)
    def delete_user(self):
        self.client.delete("/users/1")