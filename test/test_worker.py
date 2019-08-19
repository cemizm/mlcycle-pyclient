import mlcycle
import dataclasses
import unittest

from httmock import all_requests, HTTMock

@all_requests
def get_all(url, request):
    return {'status_code': 200,'content': '[{"name": "Worker 1","id": "4efab54c-1571-480f-b4dc-d7c00948b7f8"}]'}

@all_requests
def get_by_id(url, request):
    return {'status_code': 200,'content': '{"name": "Worker 1","id": "4efab54c-1571-480f-b4dc-d7c00948b7f8"}'}

@all_requests
def add(url, requests):
    return {'status_code': 200,'content': '{"name": "Worker 1","id": "4efab54c-1571-480f-b4dc-d7c00948b7f8"}'}

@all_requests
def update(url, requests):
    return {'status_code': 200,'content': '{"name": "Worker 2","id": "4efab54c-1571-480f-b4dc-d7c00948b7f8"}'}

@all_requests
def delete(url, requests):
    return {'status_code': 200}


class TestWorker(unittest.TestCase):
    def setUp(self):
        self.client = mlcycle.init_with("https://192.168.99.100:5001/api")

    def test_get_all(self):
        with HTTMock(get_all):
            worker = mlcycle.models.Worker(name="Worker 1", id="4efab54c-1571-480f-b4dc-d7c00948b7f8")
            resp = self.client.Workers.get_all()
            self.assertTrue(dataclasses.is_dataclass(resp[0]))
            self.assertEqual(resp[0], worker)

    def test_get_by_id(self):
        with HTTMock(get_by_id):
            worker = mlcycle.models.Worker(name="Worker 1", id="4efab54c-1571-480f-b4dc-d7c00948b7f8")
            resp = self.client.Workers.get_by_id("4efab54c-1571-480f-b4dc-d7c00948b7f8")
            self.assertTrue(dataclasses.is_dataclass(resp))
            self.assertEqual(resp, worker)

    def test_add(self):
        with HTTMock(add):
            worker = mlcycle.models.Worker(name="Worker 1", id="4efab54c-1571-480f-b4dc-d7c00948b7f8")
            resp = self.client.Workers.add(worker)
            self.assertTrue(dataclasses.is_dataclass(resp))
            self.assertEqual(resp, worker)

    def test_update(self):
        with HTTMock(update):
            worker = mlcycle.models.Worker(name="Worker 2", id="4efab54c-1571-480f-b4dc-d7c00948b7f8")
            resp = self.client.Workers.update(worker.id, worker)
            self.assertTrue(dataclasses.is_dataclass(resp))
            self.assertEqual(resp, worker)

    def test_delete(self):
        with HTTMock(delete):
            worker = mlcycle.models.Worker(name="Worker 2", id="4efab54c-1571-480f-b4dc-d7c00948b7f8")
            resp = self.client.Workers.delete(worker.id)
            self.assertTrue(resp)

    def test_check(self):
        worker = mlcycle.models.Worker(name="Worker 2", id="4efab54c-1571-480f-b4dc-d7c00948b7f8")
        self.client.Workers.check(worker)
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()