import requests

from .apierror import ApiError
from .environment import Environment


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
            json: a list of every project, False if the Request fails

        """
        resp = requests.get(self.url, verify=False)

        if resp.status_code != 200:
            return False

        return resp.json()

    def get_by_id(self, project_id):
        """Get a project with a specific id as a json

        Args:
            project_id: id of a specific project

        Return:
            json: a single project, False if the Request fails

        Raises:
            ApiError: If the project_id is not valid

        """
        if not project_id:
            raise ApiError("project_id not given")

        resp = requests.get(self.url + "/" + project_id, verify=False)

        if resp.status_code != 200:
            return False

        return resp.json()

    def add(self, project):
        """Add a project

        Args:
            project: a project you want to create as a json
                {
                "name": "Project 1",
                "gitrepository": "https://github.com/cemizm/tf-benchmark-gpu.git"
                }
        Return:
            json: returns the added project, False if the Request fails

        """
        self.check(project)

        resp = requests.post(self.url, json=project, verify=False)

        if resp.status_code != 200:
            return False

        return resp.json()

    def update(self, project_id, project):
        """Update a project with a specific ID

        Args:
            project_id: id of the project, you want to change
            project: updated version of the project, as a json
                {
                "name": "Mein Project 1",
	            "gitrepository": "https://github.com/cemizm/tf-benchmark-gpu.git"
                }
        
        Return:
            json: returns the updated project, False if the Request fails

        Raises:
            ApiError: If the project_id is not given

        """
        if not project_id:
            raise ApiError("project_id not given")

        self.check(project)

        resp = requests.put(self.url + "/" + project_id, json=project, verify=False)
        if resp.status_code != 200:
            return False

        return resp.json()

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

    def check(self, project):
        """Check if the project,name and git repository are set

        Args:
            project: the project you want to check

        Raises:
            ApiError: If the project is not set
            ApiError: If the project has no name
            ApiError: If the project has no gitrepository

        """
        if not project:
            raise ApiError("project not set")

        if 'name' not in project or project['name'] == "":
            raise ApiError("project name not set")

        if 'gitRepository' not in project or project['gitRepository'] == "":
            raise ApiError('git repository not set')
