import requests
import os

from .environment import Environment

from .worker import WorkerCollection
from .project import ProjectCollection
from .job import JobCollection
from .scheduler import Scheduler
from .fragment import FragmentCollection

requests.packages.urllib3.disable_warnings()


def from_env():
    """loads environment variables, creates an environment and creates the client

    Return:
        A Client - Object

    """
    host = os.environ.get('MLCYCLE_HOST')
    project = os.environ.get('MLCYCLE_PROJECT')
    job = os.environ.get('MLCYCLE_JOB')
    step = os.environ.get('MLCYCLE_STEP')

    env = Environment(host, project, job, step)

    return Client(env)


def init_with(host):
    """creates an environment and creates the client with only the host address

    Return:
        A Client Object

    """
    env = Environment(host)

    return Client(env)


class Client:
    """Client

    Attributes:
        env: Object of the Class Environment
        Workers: Object of the Class WorkerCollection
        Projects: Object of the Class ProjectCollection
        Jobs: Object of the Class JobCollection
        Scheduler: Object of the Class Scheduler
        Fragments: Object of the Class FragmentCollection

    """
    env: Environment

    Workers: WorkerCollection
    Projects: ProjectCollection
    Jobs: JobCollection
    Scheduler: Scheduler
    Fragments: FragmentCollection

    def __init__(self, environment):
        self.env = environment

        self.Workers = WorkerCollection(environment)
        self.Projects = ProjectCollection(environment)
        self.Jobs = JobCollection(environment)
        self.Scheduler = Scheduler(environment)
        self.Fragments = FragmentCollection(environment)
