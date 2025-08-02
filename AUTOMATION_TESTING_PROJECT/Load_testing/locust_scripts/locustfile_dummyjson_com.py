from locust import HttpUser, task, between

class DummyJsonUser(HttpUser):
    wait_time = between(1, 2)

    @task(10)
    def get_users(self):
        self.client.get("/users")

    @task(5)
    def get_user(self):
        self.client.get("/users/1")

    @task(3)
    def create_user(self):
        payload = {
            "firstName": "John",
            "lastName": "Doe",
            "age": 30,
            " occupation": "Developer"
        }
        self.client.post("/users/add", json=payload, headers={"Content-Type": "application/json"})

    @task(2)
    def update_user(self):
        payload = {
            "firstName": "Jane",
            "lastName": "Doe",
            "age": 30,
            " occupation": "Developer"
        }
        self.client.put("/users/1", json=payload, headers={"Content-Type": "application/json"})

    @task(1)
    def delete_user(self):
        self.client.delete("/users/1")