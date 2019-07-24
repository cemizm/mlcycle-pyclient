import requests

from .environment import Environment

from .worker import WorkerCollection
from .project import ProjectCollection
from .job import JobCollection
from .scheduler import Scheduler
from .fragment import FragmentCollection

requests.packages.urllib3.disable_warnings()

def from_env():
    env = Environment()

    return Client(env)

class Client:
    env:Environment

    Workers:WorkerCollection
    Projects:ProjectCollection
    Jobs:JobCollection
    Scheduler:Scheduler
    Fragments:FragmentCollection

    def __init__(self, environment):
        self.env = environment

        self.Workers = WorkerCollection(environment)
        self.Projects = ProjectCollection(environment)
        self.Jobs = JobCollection(environment)
        self.Scheduler = Scheduler(environment)
        self.Fragments = FragmentCollection(environment)