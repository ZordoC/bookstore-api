from locust import HttpUser, TaskSet, task, between


class BookstoreLocustTasks(TaskSet):
    # @task
    # def token_test(self):
    #     self.client.post("/token", dict(username="test", password="test"))

    @task
    def test_post_user(self):
        user_dict = {"name": "personel1",
                     "password": "pass1",
                     "role": "admin",
                     "mail": "a@b.com"}
        auth_header = {
            "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ0ZXN0Iiwicm9sZSI6ImFkbWluIiwiZXhwIjoxNjA3NzA4NDc5fQ.OUTGlttmGRr1EOYs1y2-PTTgs4VsFQVhBs6r-pKzhNo"}
        self.client.post("/v1/user", json=user_dict, headers=auth_header)


class BookstoreLoadTest(HttpUser):
    tasks = [BookstoreLocustTasks]
    wait_time = between(0.100, 1.500)
    host = "http://localhost:8000"


ab -n 100 -c 5 -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ0ZXN0Iiwicm9sZSI6ImFkbWluIiwiZXhwIjoxNjA3NzA4NDc5fQ.OUTGlttmGRr1EOYs1y2-PTTgs4VsFQVhBs6r-pKzhNo" -p tests/ab_jsons/post_user.json http://127.0.0.1:8000/v1/user