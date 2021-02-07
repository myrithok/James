from locust import HttpUser, task, between, tag

class WebsiteUser(HttpUser):
    wait_time = between(2, 5)

    @tag('POST')
    @task(3)
    def uploadMicro(self):
        test_request = {
            "fileCount": 1,
            "numTopics": 2
        }
        file = open('macro_micro.txt', 'r')
        self.client.post("/upload", data=test_request, files={'file0': file})

    @tag('POST')
    @task(3)
    def uploadNetflix(self):
        test_request = {
            "fileCount": 1,
            "numTopics": 2
        }
        file = open('netflix_chips.txt', 'r')
        self.client.post("/upload", data=test_request, files={'file0': file})

    @tag('GET')
    @task(1)
    def uploadGet(self):
        self.client.get(url="/upload")
