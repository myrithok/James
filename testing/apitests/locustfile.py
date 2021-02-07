from locust import HttpUser, task, between, tag
import os


# Locust creates an HTTP user which sends REST requests to the backend
# Web instance is located at http://localhost:8089
class WebsiteUser(HttpUser):
    # Each user makes a request, waits between 2-5 seconds and then makes another one
    wait_time = between(2, 5)

    # The tag is used in the command to specify which tasks to complete.
    # The task weighting (ex. 2) shows how much more often this task will be chosen.
    # A task of weight 2 gets chosen twice as often as a task with weight 1.

    # uploadTestBasic creates a POST request and sends 1 file with numtopics=2 to the
    # backend.
    @tag('POST')
    @task(3)
    def uploadTestBasic(self):
        test_request = {
            "fileCount": 1,
            "numTopics": 2
        }
        filename = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'testdata', 'testdata.txt')
        file = open(filename, 'r')
        self.client.post("/upload", data=test_request, files={'file0': file})

    # uploadTestLarge creates a POST request and sends 1 large text file (6MB)
    # with numtopics=10 to the backend.
    @tag('POST')
    @task(1)
    def uploadTestLarge(self):
        test_request = {
            "fileCount": 1,
            "numTopics": 10
        }
        filename = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'testdata', 'testdata6MB.txt')
        file = open(filename, 'r')
        self.client.post("/upload", data=test_request, files={'file0': file})

    # uploadTwoFiles creates a POST request and sends 2 files to backend.
    @tag('POST')
    @task(2)
    def uploadTwoFiles(self):
        test_request = {
            "fileCount": 2,
            "numTopics": 2
        }
        filename0 = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'testdata', 'testsentenceone.txt')
        file0 = open(filename0, 'r')
        filename1 = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'testdata', 'testsentencetwo.txt')
        file1 = open(filename1, 'r')

        self.client.post("/upload", data=test_request, files={'file0': file0, 'file1': file1})

    # uploadGet makes a simple GET request to the backend, which returns the results of
    # the LDA and sentiment model. Can be manually checked by going to http://localhost:5000/upload
    @tag('GET')
    @task(1)
    def uploadGet(self):
        self.client.get(url="/upload")
