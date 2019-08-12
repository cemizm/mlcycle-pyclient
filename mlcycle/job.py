import requests
import dataclasses

from .apierror import ApiError
from .environment import Environment
from .models import Job, Project, Step, DockerConfiguration, DockerBuildConfiguration


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
            without fragments of steps
        
        Return:
            json: a list of Job objects, False if the Request fails

        """
        resp = requests.get(self.url, verify=False)

        if resp.status_code != 200:
            return False

        job_list = []
        for elem in resp.json():
            job_list.append(Job(**elem))
        return job_list

    def get_by_id(self, job_id):
        """Get a Job with a specific id as a json
            with fragments of steps

        Args:
            job_id: id of a specific job

        Return:
            json: a job object, False if the Request fails

        Raises:
            ApiError: If the job_id is not valid

        """
        if not job_id:
            raise ApiError("job_id not given")

        resp = requests.get(self.url + "/" + job_id, verify=False)

        if resp.status_code != 200:
            return False

        return Job(**resp.json())

    def add_steps(self, job_id, steps):
        """Add steps to a specific job

        Args:
            job_id: the id of a specific job, where steps will be added
            steps: a list of one or more steps, you want to add to the job

        Return:
            object of the updated job, False if the Request fails

        Raises:
            ApiError: If the Attributes are not set properly

        """
        if not job_id:
            raise ApiError("job_id not given")

        if not steps or len(steps) == 0:
            raise ApiError("No steps given")

        step_list = []

        for step in steps:
            if not step.name:
                raise ApiError("step name not set")
            if not step.docker:
                raise ApiError("docker configuration not set")

            docker = step.docker

            if not docker.image:
                if not docker.build_configuration:
                    raise ApiError("neither an image nor a build configuration is set")

                build = docker.build_configuration

                if not build.dockerfile:
                    raise ApiError("dockerfile for build configuration not set")

            step_list.append(dataclasses.asdict(step))

        resp = requests.post(self.url + "/" + job_id + "/steps", json=step_list, verify=False)

        if resp.status_code != 200:
            return False

        return Job(**resp.json())

    def add_metrics(self, metrics, job_id=None, step=None):
        """Add metrics to a step of a specific job

        Just for visualisation purposes in the terminal, it has no actual
        functionality

        Args:
            metrics: the metrics you want to add
            job_id: the id of a specific job, by default it is none and gets
                the step from the environment
            step: (number)the step to which you want to add metrics, by default it is
                none and gets the step from the environment

        Return:
            object of the updated job, False if the Request fails

        Raises:
            ApiError: If the Attributes are not set properly

        """
        if not job_id and not step:
            job_id = self.env.get_job()
            step = self.env.get_step()

        
        if not job_id:
            raise ApiError("job_id not given")

        if not str(step):
            raise ApiError("step not given")

        if not metrics or len(metrics) == 0:
            raise ApiError("No metrics given")

        resp = requests.post(self.url + "/" + job_id + "/step/" + str(step) + "/metrics", json=metrics, verify=False)

        if resp.status_code != 200:
            return False

        return Job(**resp.json())

    def trigger(self, project_id):
        """Start the pipeline of a specific project

        Args:
            project_id: the specific project you want to start

        Return:
            object of the started job, False if the Request fails

        Raises:
            ApiError: If the project_id is not given

        """
        if not project_id:
            raise ApiError("project_id not given")

        resp = requests.post(self.url + "/project/" + project_id + "/trigger", verify=False)

        if resp.status_code != 200:
            return False
        return Job(**resp.json())
