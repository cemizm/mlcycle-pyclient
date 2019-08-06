import requests

from .apierror import ApiError
from .environment import Environment


class FragmentCollection:
    """A Collection of Fragments

    Attributes:
        env: Object of the Environment class
        url: base url for the Request on fragments

    """
    env: Environment

    def __init__(self, env):
        self.env = env

        self.url = self.env.get_base_url() + "/fragments"

    def get_all_by_job(self, job_id):
        """Get all fragments of a specific job as a json

        Args:
            job_id: id of a specific job

        Return:
            json: a list of fragments of the specific job

        Raises:
            ApiError: If the job_id is not given

        """
        if not job_id:
            raise ApiError("job_id not given")

        resp = requests.get(self.url + "/job/" + job_id, verify=False)

        if resp.status_code != 200:
            return False

        return resp.json()

    def get_all_by_step(self, job_id, step):
        """Get all fragments of a specific job and a specific step as a json

        Args:
            job_id: id of a specific job
            step: id of a specific step

        Return:
            json: a list of fragments of the specific job and step

        Raises:
            ApiError: If the job_id is not given

        """
        if not job_id:
            raise ApiError("job_id not given")

        resp = requests.get(self.url + "/job/" + job_id + "/step/" + str(step), verify=False)

        if resp.status_code != 200:
            return False

        return resp.json()


    def get_latest_by_job(self, name, handle, job_id=None):
        """Get all fragments of a specific job with a specific name and downloads them

        Args:
            job_id: id of a specific job, by default it is none and gets
                the job from the environment
            name: name of a specific fragment
            handle: a filehandler in write mode

        Return:
            True if the download succeeds, False otherwise

        Raises:
            ApiError: If the parameters are not properly set

        """
        if not job_id:
            job_id = self.env.getJob()

        if not job_id:
            raise ApiError("job_id not given")

        if not name:
            raise ApiError("name not given")

        if not handle:
            raise ApiError("handle not given")

        resp = requests.get(self.url + "/job/" + job_id + "/name/" + name, verify=False)
        return self.__download__(resp, handle)


    def get_latest_by_project(self, project_id, name, handle):
        """Get all fragments of a specific project with a specific name and downloads them

        Args:
            project_id: id of a specific project, by default it is none and gets
                the project from the environment
            name: name of a specific fragment
            handle: a filehandler in write mode

        Return:
            True if the download succeeds, False otherwise

        Raises:
            ApiError: If the parameters are not properly set

        """
        if not project_id:
            raise ApiError("project_id not given")

        if not name:
            raise ApiError("name not given")

        if not handle:
            raise ApiError("file handle not given")

        resp = requests.get(self.url + "/project/" + project_id + "/name/" + name, stream=True, verify=False)
        return self.__download__(resp, handle)


    def get_by_id(self, fragment_id, handle):
        """Get a specific fragment and downloads it

        Args:
            fragment_id: a specific fragment, you want to download
            handle: a filehandler in write mode

        Return:
            True if the download succeeds, False otherwise

        Raises:
            ApiError: If the parameters are not properly set

        """
        if not fragment_id:
            raise ApiError("fragment_id not given")

        if not handle:
            raise ApiError("file handle not given")

        resp = requests.get(self.url + "/" + fragment_id, stream=True, verify=False)
        return self.__download__(resp, handle)


    def upload(self, fragment, handle, job_id=None, step=None):
        """Uploads fragments

        Args:
            fragment: fragment with at least the following attributes
                {
                "name": "Console Log",
                "filename": "0_console.log"
                "type": 1
                }
            handle: a filehandler in read mode
            job_id: id of a specific job, by default it is none and gets
                the job from the environment
            step: the current step, by default it is none and gets
                the current step from the environment

        Return:
            json: response of the successfull request, False otherwise

        Raises:
            ApiError: If the parameters are not properly set

        """
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
        """Writes a response into a file

        Args:
            resp: response of a request
            handle: a filehandler in write mode

        Return:
            True, but False if the Response has a statuscode of 200

        """
        #write handle
        if resp.status_code != 200:
            return False

        for chunk in resp.iter_content(chunk_size=1024):
            if not chunk:
                continue

            handle.write(chunk)
            handle.flush()

        return True
