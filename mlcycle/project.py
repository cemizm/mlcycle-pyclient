import requests
import dataclasses

from .apierror import ApiError
from .environment import Environment
from .models import Project


class ProjectCollection:
    """A Collection of Projects

    Attributes:
        env: Object of the Environment class
        url: base url for the Request on projects

    """
    env: Environment

    def __init__(self, env):
        self.env = env

        self.url = self.env.get_base_url() + "/projects"

    def get_all(self):
        """Get all projects as a json

        Return:
            a list of Project Objects, False if the Request fails

        """
        resp = requests.get(self.url, verify=False)

        if resp.status_code != 200:
            return False

        project_list = []

        for elem in resp.json():
            project_list.append(Project(**elem))
        return project_list

    def get_by_id(self, project_id):
        """Get a project with a specific id as a json

        Args:
            project_id: id of a specific project

        Return:
            a project object, False if the Request fails

        Raises:
            ApiError: If the project_id is not valid

        """
        if not project_id:
            raise ApiError("project_id not given")

        resp = requests.get(self.url + "/" + project_id, verify=False)

        if resp.status_code != 200:
            return False

        return Project(**resp.json())

    def add(self, project: Project):
        """Add a project

        Args:
            project: a project object

        Return:
            returns the added project object, False if the Request fails

        """
        self.check(project)

        project_json = {"name": project.name, "gitRepository": project.git_repository}

        resp = requests.post(self.url, json=project_json, verify=False)

        if resp.status_code != 200:
            return False

        return Project(**resp.json())

    def update(self, project_id, project: Project):
        """Update a project with a specific ID

        Args:
            project_id: id of the project, you want to change
            project: updated version of the project, as an object
        
        Return:
            returns the updated project object, False if the Request fails

        Raises:
            ApiError: If the project_id is not given

        """
        if not project_id:
            raise ApiError("project_id not given")

        self.check(project)

        project_json = {"name": project.name, "gitRepository": project.git_repository}

        resp = requests.put(self.url + "/" + project_id, json=project_json, verify=False)
        if resp.status_code != 200:
            return False

        return Project(**resp.json())

    def delete(self, project_id):
        """Delete a project with a specific ID

        Args:
            project_id: id of the project, you want to delete
        
        Return:
            json: returns the status code of the request

        Raises:
            ApiError: If the project_id is not given

        """
        if not project_id:
            raise ApiError("project_id ist not given")

        resp = requests.delete(self.url + "/" + project_id, verify=False)

        return resp.status_code == 200

    def check(self, project: Project):
        """Check if the project,name and git repository are set

        Args:
            project: the project you want to check

        Raises:
            ApiError: If the project is not a dataclass
            ApiError: If the project has no name
            ApiError: If the project has no gitrepository

        """

        if not dataclasses.is_dataclass(project):
            raise ApiError("project not a dataclass")

        if project.name == "" or project.name == None:
            raise ApiError("project name not set")

        if project.git_repository == "" or project.git_repository == None:
            raise ApiError('git repository not set')
