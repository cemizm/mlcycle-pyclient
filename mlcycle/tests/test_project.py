import mlcycle
import dataclasses
import unittest

from httmock import all_requests, HTTMock


@all_requests
def get_all(url, request):
    return {'status_code': 200,'content': '[{"name": "Project 1","gitRepository": "https://github.com/cemizm/tf-benchmark-gpu.git","id": "97df69fb-8fe1-48a1-835f-c0d699789a78"}]'}

@all_requests
def get_by_id(url, request):
    return {'status_code': 200,'content': '{"name": "Project 1","gitRepository": "https://github.com/cemizm/tf-benchmark-gpu.git","id": "97df69fb-8fe1-48a1-835f-c0d699789a78"}'}

@all_requests
def add(url, requests):
    return {'status_code': 200,'content': '{"name": "Project 1","gitRepository": "https://github.com/cemizm/tf-benchmark-gpu.git","id": "97df69fb-8fe1-48a1-835f-c0d699789a78"}'}

@all_requests
def update(url, requests):
    return {'status_code': 200,'content': '{"name": "Project 2","gitRepository": "https://github.com/cemizm/tf-benchmark-gpu.git","id": "97df69fb-8fe1-48a1-835f-c0d699789a78"}'}

@all_requests
def delete(url, requests):
    return {'status_code': 200}


class TestProject(unittest.TestCase):
    def setUp(self):
        self.client = mlcycle.init_with("https://192.168.99.100:5001/api")

    def test_get_all(self):
        with HTTMock(get_all):
            project = mlcycle.models.Project(name="Project 1", gitRepository="https://github.com/cemizm/tf-benchmark-gpu.git", id="97df69fb-8fe1-48a1-835f-c0d699789a78")
            resp = self.client.Projects.get_all()
            self.assertTrue(dataclasses.is_dataclass(resp[0]))
            self.assertEqual(resp[0], project)

    def test_get_by_id(self):
        with HTTMock(get_by_id):
            project = mlcycle.models.Project(name="Project 1", gitRepository="https://github.com/cemizm/tf-benchmark-gpu.git", id="97df69fb-8fe1-48a1-835f-c0d699789a78")
            resp = self.client.Projects.get_by_id("4efab54c-1571-480f-b4dc-d7c00948b7f8")
            self.assertTrue(dataclasses.is_dataclass(resp))
            self.assertEqual(resp, project)

    def test_add(self):
        with HTTMock(add):
            project = mlcycle.models.Project(name="Project 1", gitRepository="https://github.com/cemizm/tf-benchmark-gpu.git", id="97df69fb-8fe1-48a1-835f-c0d699789a78")
            resp = self.client.Projects.add(project)
            self.assertTrue(dataclasses.is_dataclass(resp))
            self.assertEqual(resp, project)

    def test_update(self):
        with HTTMock(update):
            project = mlcycle.models.Project(name="Project 2", gitRepository="https://github.com/cemizm/tf-benchmark-gpu.git", id="97df69fb-8fe1-48a1-835f-c0d699789a78")
            resp = self.client.Projects.update(project.id, project)
            self.assertTrue(dataclasses.is_dataclass(resp))
            self.assertEqual(resp, project)

    def test_delete(self):
        with HTTMock(delete):
            project = mlcycle.models.Project(name="Project 2", gitRepository="https://github.com/cemizm/tf-benchmark-gpu.git", id="97df69fb-8fe1-48a1-835f-c0d699789a78")
            resp = self.client.Projects.delete(project.id)
            self.assertTrue(resp)

    def test_check(self):
        project = mlcycle.models.Project(name="Project 2", gitRepository="https://github.com/cemizm/tf-benchmark-gpu.git", id="97df69fb-8fe1-48a1-835f-c0d699789a78")
        self.client.Projects.check(project)
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()