import requests

from .apierror import ApiError
from .environment import Environment


class JobCollection:
    env: Environment

    def __init__(self, env):
        self.env = env

        self.url = self.env.get_base_url() + "/jobs"

    def get_all(self):
        resp = requests.get(self.url, verify=False)

        if resp.status_code != 200:
            return False

        return resp.json()

    def get_by_id(self, job_id):
        if not job_id:
            raise ApiError("job_id not given")

        resp = requests.get(self.url + "/" + job_id, verify=False)

        if resp.status_code != 200:
            return False

        return resp.json()

    def add_steps(self, job_id, steps):
        if not job_id:
            raise ApiError("job_id not given")

        if not steps or len(steps) == 0:
            raise ApiError("No steps given")

        for step in steps:
            if "name" not in step:
                raise ApiError("step name not set")
            if "docker" not in step:
                raise ApiError("docker configuration not set")

            docker = step['docker']

            if "image" not in docker:
                if "buildConfiguration" not in docker:
                    raise ApiError("neither an image nor a build configuration is set")

                build = docker['buildConfiguration']

                if "dockerfile" not in build:
                    raise ApiError("dockerfile for build configuration not set")

        resp = requests.post(self.url + "/" + job_id + "/steps", json=steps, verify=False)

        if resp.status_code != 200:
            return False

        return resp.json()

    def add_metrics(self, metrics, job_id=None, step=None):
        if not job_id and not step:
            job_id = self.env.getJob()
            step = self.env.getStep()

        if not job_id:
            raise ApiError("jobId not given")

        if not str(step):
            raise ApiError("step not given")

        if not metrics or len(metrics) == 0:
            raise ApiError("No steps given")

        resp = requests.post(self.url + "/" + job_id + "/step/" + str(step) + "/metrics", json=metrics, verify=False)

        if resp.status_code != 200:
            return False

        return resp.json()

    def trigger(self, project_id):
        if not project_id:
            raise ApiError("project_id not given")

        resp = requests.post(self.url + "/project/" + project_id + "/trigger", verify=False)

        if resp.status_code != 200:
            return False

        return resp.json()
