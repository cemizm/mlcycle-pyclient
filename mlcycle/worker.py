import requests

from .apierror import ApiError
from .environment import Environment


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
        """Get all workers as a json

        Return:
            json: a list of every worker, False if the Request fails

        """
        resp = requests.get(self.url, verify=False)

        if resp.status_code != 200:
            return False

        return resp.json()

    def get_by_id(self, worker_id):
        """Get a worker with a specific id as a json

        Args:
            worker_id: id of a specific worker

        Return:
            json: a single worker, False if the Request fails

        Raises:
            ApiError: If the worker_id is not valid

        """
        if not worker_id:
            raise ApiError("worker_id not given")

        resp = requests.get(self.url + "/" + worker_id, verify=False)

        if resp.status_code != 200:
            return False

        return resp.json()

    def add(self, worker):
        """Add a worker

        Args:
            worker: a worker you want to create as a json
                {"name": "Worker 1"}
        
        Return:
            json: returns the added worker, False if the Request fails

        """
        self.check(worker)

        resp = requests.post(self.url, json=worker, verify=False)

        if resp.status_code != 200:
            return False

        return resp.json()

    def update(self, worker_id, worker):
        """Update a Worker with a specific ID

        Args:
            worker: updated version of the worker, as a json
                {"name": "Worker new"}
            worker_id: id of the worker, you want to change
        
        Return:
            json: returns the updated worker, False if the Request fails

        Raises:
            ApiError: If the worker_id is not given

        """
        if not worker_id:
            raise ApiError("worker_id not given")

        self.check(worker)

        resp = requests.put(self.url + "/" + worker_id, json=worker, verify=False)
        if resp.status_code != 200:
            return False

        return resp.json()

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

    def check(self, worker):
        """Check if the worker and his name are set

        Args:
            worker: the worker you want to check

        Raises:
            ApiError: If the worker is not set
            ApiError: If the worker has no name

        """
        if not worker:
            raise ApiError("worker not set")

        if 'name' not in worker or worker['name'] == "":
            raise ApiError("worker name not set")
