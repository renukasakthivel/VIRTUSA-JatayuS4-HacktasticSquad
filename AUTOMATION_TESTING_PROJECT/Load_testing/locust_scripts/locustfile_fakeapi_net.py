from locust import HttpUser, task, between

class FakeApiUser(HttpUser):
    wait_time = between(1, 2)

    @task(10)
    def get_users(self):
        self.client.get("/api/users")

    @task(5)
    def get_user(self):
        self.client.get("/api/users/1")

    @task(3)
    def post_user(self):
        payload = {
            "name": "John Doe",
            "email": "johndoe@example.com"
        }
        headers = {
            "Content-Type": "application/json"
        }
        self.client.post("/api/users", json=payload, headers=headers)

    @task(2)
    def put_user(self):
        payload = {
            "name": "Jane Doe",
            "email": "janedoe@example.com"
        }
        headers = {
            "Content-Type": "application/json"
        }
        self.client.put("/api/users/1", json=payload, headers=headers)

    @task(1)
    def delete_user(self):
        self.client.delete("/api/users/1")