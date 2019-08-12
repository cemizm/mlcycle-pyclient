import requests

from .apierror import ApiError
from .environment import Environment
from .models import Job


class Scheduler:
    """Scheduler

    Attributes:
        env: Object of the Environment class
        url: base url for Requests on the Scheduler

    """
    env: Environment
    url = None

    def __init__(self, env):
        self.env = env
        self.url = self.env.get_base_url() + "/scheduler"

    def get_pending(self):
        """get all pending steps of a job of a project

        Return:
            a list of Job Objects, or an empty array if the request has a
            timeout or False if the Request fails

        """
        resp = requests.get(self.url, verify=False)

        if resp.status_code == 408:
            return []
        elif resp.status_code != 200:
            return False

        job_list = []
        for elem in resp.json():
            job_list.append(Job(**elem))
        return job_list

    def claim(self, job_id, step):
        """Claim a step of a specific job

        Args:
            job_id: id of a specific job
            step: number of the step
            
        Return:
            True on success, False otherwise

        Raises:
            ApiError: If the job_id or step are not given

        """
        self.check(job_id, step)

        resp = requests.post(self.url + "/" + job_id + "/step/" + str(step) + "/claim", verify=False)

        return resp.status_code == 200

    def complete(self, job_id, step):
        """Complete a step of a specific job

        Args:
            job_id: id of a specific job
            step: number of the step

        Return:
            True on success, False otherwise

        Raises:
            ApiError: If the job_id or step are not given

        """
        self.check(job_id, step)

        resp = requests.post(self.url + "/" + job_id + "/step/" + str(step) + "/complete", verify=False)

        return resp.status_code == 200

    def error(self, job_id, step):
        """Fail a step of a specific job

        Args:
            job_id: id of a specific job
            step: number of the step

        Return:
            True on success, False otherwise

        Raises:
            ApiError: If the job_id or step are not given

        """
        self.check(job_id, step)

        resp = requests.post(self.url + "/" + job_id + "/step/" + str(step) + "/error", verify=False)

        return resp.status_code == 200

    def check(self, job_id, step):
        """Check, if job_id and step are set

        Args:
            job_id: id of a specific job
            step: number of the step

        Raises:
            ApiError: If the job_id or step are not given

        """
        if not job_id:
            raise ApiError("job_id not set")

        if not str(step):
            raise ApiError("step not set")
