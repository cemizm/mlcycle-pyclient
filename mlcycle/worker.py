import requests

from .apierror import ApiError
from .environment import Environment


class WorkerCollection:
    env: Environment

    def __init__(self, env):
        self.env = env

        self.url = self.env.get_base_url() + "/workers"

    def get_all(self):
        resp = requests.get(self.url, verify=False)

        if resp.status_code != 200:
            return False

        return resp.json()

    def get_by_id(self, worker_id):
        if not worker_id:
            raise ApiError("workerId not given")

        resp = requests.get(self.url + "/" + worker_id, verify=False)

        if resp.status_code != 200:
            return False

        return resp.json()

    def add(self, worker):
        self.check(worker)

        resp = requests.post(self.url, json=worker, verify=False)

        if resp.status_code != 200:
            return False

        return resp.json()

    def update(self, worker_id, worker):
        if not worker_id:
            raise ApiError("workerId not given")

        self.check(worker)

        resp = requests.put(self.url + "/" + worker_id, json=worker, verify=False)
        if resp.status_code != 200:
            return False

        return resp.json()

    def delete(self, worker_id):
        if not worker_id:
            raise ApiError("workerId is not given")

        resp = requests.delete(self.url + "/" + worker_id, verify=False)

        return resp.status_code == 200

    def check(self, worker):
        if not worker:
            raise ApiError("worker not set")

        if 'name' not in worker or worker['name'] == "":
            raise ApiError("worker name not set")
