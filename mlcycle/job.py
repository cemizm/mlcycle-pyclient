import requests

from .apierror import ApiError
from .environment import Environment


class JobCollection:
    """A Collection of Jobs

    Attributes:
        env: Object of the Environment class
        url: base url for the Request on jobs

    """
    env: Environment

    def __init__(self, env):
        self.env = env

        self.url = self.env.get_base_url() + "/jobs"

    def get_all(self):
        """Get all existing jobs
        
        Return:
            json: a list of every Job, False if the Request fails

        """
        resp = requests.get(self.url, verify=False)

        if resp.status_code != 200:
            return False

        return resp.json()

    def get_by_id(self, job_id):
        """Get a Job with a specific id as a json

        Args:
            job_id: id of a specific job

        Return:
            json: a single job, False if the Request fails

        Raises:
            ApiError: If the job_id is not valid

        """
        if not job_id:
            raise ApiError("job_id not given")

        resp = requests.get(self.url + "/" + job_id, verify=False)

        if resp.status_code != 200:
            return False

        return resp.json()

    def add_steps(self, job_id, steps):
        """Add steps to a specific job

        Args:
            job_id: the id of a specific job, where steps will be added
            steps: a list of one or more steps, you want to add to the job

        Return:
            json: the updated job, False if the Request fails

        Raises:
            ApiError: If the Attributes are not set properly

        """
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
        """Add metrics to a step of a specific job

        Just for visualisation purposes in the terminal, it has no actual
        functionality

        Args:
            metrics: the metrics you want to add
            job_id: the id of a specific job, by default it is none and gets
                the step from the environment
            step: the step to which you want to add metrics, by default it is
                none and gets the step from the environment

        Return:
            json: the updated job, False if the Request fails

        Raises:
            ApiError: If the Attributes are not set properly

        """
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
        """Start the pipeline of a specific project

        Args:
            project_id: the specific project you want to start

        Return:
            json: the started job, False if the Request fails

        Raises:
            ApiError: If the project_id is not given

        """
        if not project_id:
            raise ApiError("project_id not given")

        resp = requests.post(self.url + "/project/" + project_id + "/trigger", verify=False)

        if resp.status_code != 200:
            return False

        return resp.json()
