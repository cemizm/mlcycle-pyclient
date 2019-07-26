import requests

from .apierror import ApiError
from .environment import Environment


class FragmentCollection:
    env: Environment

    def __init__(self, env):
        self.env = env

        self.url = self.env.get_base_url() + "/fragments"

    def get_all_by_job(self, job_id):
        if not job_id:
            raise ApiError("job_id not given")

        resp = requests.get(self.url + "/job/" + job_id, verify=False)

        if resp.status_code != 200:
            return False

        return resp.json()

    def get_all_by_step(self, job_id, step):
        if not job_id:
            raise ApiError("job_id not given")

        resp = requests.get(self.url + "/job/" + job_id + "/step/" + str(step), verify=False)

        if resp.status_code != 200:
            return False

        return resp.json()


def get_latest_by_job(self, name, handle, job_id=None):
    if not job_id:
        job_id = self.env.getJob()

    if not job_id:
        raise ApiError("jobId not given")

    if not name:
        raise ApiError("name not given")

    if not handle:
        raise ApiError("name not given")

    resp = requests.get(self.url + "/job/" + job_id + "/name/" + name, verify=False)
    return self.__download__(resp, handle)


def get_latest_by_project(self, project_id, name, handle):
    if not project_id:
        raise ApiError("project_id not given")

    if not name:
        raise ApiError("name not given")

    if not handle:
        raise ApiError("file handle not given")

    resp = requests.get(self.url + "/project/" + project_id + "/name/" + name, stream=True, verify=False)
    return self.__download__(resp, handle)


def get_by_id(self, fragment_id, handle):
    if not fragment_id:
        raise ApiError("fragment_id not given")

    if not handle:
        raise ApiError("file handle not given")

    resp = requests.get(self.url + "/" + fragment_id, stream=True, verify=False)
    return self.__download__(resp, handle)


def upload(self, fragment, handle, job_id=None, step=None):
    if not job_id and not step:
        job_id = self.env.getJob()
        step = self.env.getStep()

    if not job_id:
        raise ApiError("job_id not given")

    if "name" not in fragment:
        raise ApiError("name not in fragment")

    if "filename" not in fragment:
        raise ApiError("filename not in fragment")

    if "type" not in fragment:
        raise ApiError("type not in fragment")

    data = {
        "Name": fragment['name'],
        "Filename": fragment['filename'],
        "Type": fragment['type']
    }
    files = {
        "BinaryData": handle
    }

    resp = requests.post(self.url + "/job/" + job_id + "/step/" + str(step), data=data, files=files, verify=False)

    if resp.status_code != 200:
        print(resp.text)
        return False

    return resp.json()


def __download__(self, resp, handle):
    if resp.status_code != 200:
        return False

    for chunk in resp.iter_content(chunk_size=1024):
        if not chunk:
            continue

        handle.write(chunk)
        handle.flush()

    return True
