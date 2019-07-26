import requests

from .apierror import ApiError
from .environment import Environment


class ProjectCollection:
    env: Environment

    def __init__(self, env):
        self.env = env

        self.url = self.env.get_base_url() + "/projects"

    def get_all(self):
        resp = requests.get(self.url, verify=False)

        if resp.status_code != 200:
            return False

        return resp.json()

    def get_by_id(self, project_id):
        if not project_id:
            raise ApiError("project_id not given")

        resp = requests.get(self.url + "/" + project_id, verify=False)

        if resp.status_code != 200:
            return False

        return resp.json()

    def add(self, project):
        self.check(project)

        resp = requests.post(self.url, json=project, verify=False)

        if resp.status_code != 200:
            return False

        return resp.json()

    def update(self, project_id, project):
        if not project_id:
            raise ApiError("project_id not given")

        self.check(project)

        resp = requests.put(self.url + "/" + project_id, json=project, verify=False)
        if resp.status_code != 200:
            return False

        return resp.json()

    def delete(self, project_id):
        if not project_id:
            raise ApiError("project_id ist not given")

        resp = requests.delete(self.url + "/" + project_id, verify=False)

        return resp.status_code == 200

    def check(self, project):
        if not project:
            raise ApiError("project not set")

        if 'name' not in project or project['name'] == "":
            raise ApiError("project name not set")

        if 'gitRepository' not in project or project['gitRepository'] == "":
            raise ApiError('git repository not set')
