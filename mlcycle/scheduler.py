import requests

from .apierror import ApiError
from .environment import Environment


class Scheduler:
    env: Environment
    url = None

    def __init__(self, env):
        self.env = env
        self.url = self.env.get_base_url() + "/scheduler"

    def get_pending(self):
        resp = requests.get(self.url, verify=False)

        if resp.status_code == 408:
            return []
        elif resp.status_code != 200:
            return False

        return resp.json()

    def claim(self, job_id, step):
        self.check(job_id, step)

        resp = requests.post(self.url + "/" + job_id + "/step/" + str(step) + "/claim", verify=False)

        return resp.status_code == 200

    def complete(self, job_id, step):
        self.check(job_id, step)

        resp = requests.post(self.url + "/" + job_id + "/step/" + str(step) + "/complete", verify=False)

        return resp.status_code == 200

    def error(self, job_id, step):
        self.check(job_id, step)

        resp = requests.post(self.url + "/" + job_id + "/step/" + str(step) + "/error", verify=False)

        return resp.status_code == 200

    def check(self, job_id, step):
        if not job_id:
            raise ApiError("job_id not set")

        if not str(step):
            raise ApiError("step not set")
