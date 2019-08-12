from dataclasses import dataclass
from enum import Enum


class ProcessingState(Enum):
    CREATED = 0
    INPROGRESS = 1
    DONE = 2
    SCHEDULED = 21
    ERROR = 31

class FragmentType(Enum):
    METRICS = 0
    BUILDLOGS = 1
    MODEL = 2

class JobInitiator(Enum):
    MANUAL = 0
    GIT = 1
    DATA = 2

@dataclass
class Project:
    name:str
    git_repository:str
    id:str = None

    def __init__(self, name: str, gitRepository: float, id: str=None):
        self.name = name
        self.git_repository = gitRepository
        self.id = id


@dataclass
class Worker:
    name:str
    id:str = None

    def __init__(self, name: str, id: str=None):
        self.name = name
        self.id = id

@dataclass
class Fragment:
    created:str
    filename:str
    type:FragmentType
    name:str = None
    step_number:int = None
    job_id:str = None
    id:str = None

    def __init__(self, created: str, filename: str, type: FragmentType,
            name:str=None, stepNumber: int=None, jobId: str=None, id: str=None):
        self.name = name
        self.step_number = stepNumber
        self.created = created
        self.filename = filename
        self.type = type
        self.job_id = jobId
        self.id = id

@dataclass
class DockerBuildConfiguration:
    context:str
    dockerfile:str
    properties:dict=None

    def __init__(self, context: str, dockerfile: str, properties: dict=None):
        self.context = context
        self.dockerfile = dockerfile
        self.properties = properties
        
@dataclass
class DockerConfiguration:
    command:str
    image:str=None
    build_configuration:DockerBuildConfiguration=None
    properties:dict=None

    def __init__(self, command: str, image: str=None,
            buildConfiguration: dict=None, properties: dict=None):
        self.command = command
        self.image = image
        if buildConfiguration is None:
            self.build_configuration = None
        else:
            self.build_configuration = DockerBuildConfiguration(**buildConfiguration)
        self.properties = properties

@dataclass
class Step:
    name:str
    number:int = None
    state:ProcessingState = None
    start:str = None
    end:str = None
    docker:DockerConfiguration = None
    metrics:dict = None
    fragments:[Fragment] = None
    id:str = None

    def __init__(self, name: str, number: int=None, state: ProcessingState=None, 
        start: str=None, end: str=None, docker: dict=None, 
        metrics: dict=None, fragments:dict=None, id: str=None):
        self.name = name
        self.number = number
        self.state = state
        self.start = start
        self.end = end
        if docker is None:
            self.docker = None
        else:
            self.docker = DockerConfiguration(**docker)
        self.metrics = metrics
        if fragments is None:
            self.fragments = None
        else:
            self.fragments = []
            for fragment in fragments:
                self.fragments.append(Fragment(**fragment))
        self.id = id

@dataclass
class Job:
    initiator:JobInitiator
    state:ProcessingState = None
    steps:[Step] = None
    project:Project = None
    project_id:str = None
    created:str = None
    finished:str = None
    id:str = None

    def __init__(self, initiator: JobInitiator, state: ProcessingState=None,
            steps: [dict]=None, project: dict=None, projectId: str=None,
            created: str=None, finished: str=None, step: Step=None, id: str=None,
            jobId: str=None):
        self.state = state
        self.initiator = initiator
        self.steps = []
        if step is not None:
            self.steps.append(Step(**step))
        if steps is not None:
            for step in steps:
                self.steps.append(Step(**step))
        if project is None:
            self.project = None
        else:
            self.project = Project(**project)
        self.project_id = projectId
        self.created = created
        self.finished = finished
        if jobId is not None:
            self.id = jobId
        if id is not None:
            self.id = id