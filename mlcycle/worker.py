import requests
import dataclasses

from .apierror import ApiError
from .environment import Environment
from .models import Worker


class WorkerCollection:
    """A Collection of Workers

    Attributes:
        env: Object of the Environment class
        url: base url for the Request on workers

    """
    env: Environment

    def __init__(self, env):
        self.env = env

        self.url = self.env.get_base_url() + "/workers"

    def get_all(self):
        """Get a list of worker objects

        Return:
            a list of Worker Objects, False if the Request fails

        """
        resp = requests.get(self.url, verify=False)

        if resp.status_code != 200:
            return False
        
        worker_list = []

        for elem in resp.json():
            worker_list.append(Worker(**elem))
        return worker_list

    def get_by_id(self, worker_id):
        """Get a worker with a specific id as a json

        Args:
            worker_id: id of a specific worker

        Return:
            a worker object, False if the Request fails

        Raises:
            ApiError: If the worker_id is not valid

        """
        if not worker_id:
            raise ApiError("worker_id not given")

        resp = requests.get(self.url + "/" + worker_id, verify=False)

        if resp.status_code != 200:
            return False

        return Worker(**resp.json())

    def add(self, worker: Worker):
        """Add a worker

        Args:
            worker: a worker object
        
        Return:
            returns the successfully added worker object, False if the Request fails

        """
        self.check(worker)

        worker_json = {"name": worker.name}

        resp = requests.post(self.url, json=worker_json, verify=False)

        if resp.status_code != 200:
            return False

        return Worker(**resp.json())

    def update(self, worker_id, worker: Worker):
        """Update a Worker with a specific ID

        Args:
            worker_id: id of the worker, you want to change
            worker: updated version of the worker, as an object
        
        Return:
            returns the updated worker object, False if the Request fails

        Raises:
            ApiError: If the worker_id is not given

        """
        if not worker_id:
            raise ApiError("worker_id not given")

        self.check(worker)
        
        worker_json = {"name": worker.name}

        resp = requests.put(self.url + "/" + worker_id, json=worker_json, verify=False)
        if resp.status_code != 200:
            return False

        return Worker(**resp.json())

    def delete(self, worker_id):
        """Delete a Worker with a specific ID

        Args:
            worker_id: id of the worker, you want to delete
        
        Return:
            json: returns the status code of the request

        Raises:
            ApiError: If the worker_id is not given

        """
        if not worker_id:
            raise ApiError("worker_id is not given")

        resp = requests.delete(self.url + "/" + worker_id, verify=False)

        return resp.status_code == 200

    def check(self, worker: Worker):
        """Check if the worker and his name are set

        Args:
            worker: the worker you want to check

        Raises:
            ApiError: If the worker is not a dataclass
            ApiError: If the worker has no name

        """
        if not dataclasses.is_dataclass(worker):
            raise ApiError("worker not a dataclass")

        if worker.name == "" or worker.name == None:
            raise ApiError("worker name not set")
