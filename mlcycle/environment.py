import os

class Environment:
    host = None
    project = None
    job = None
    step = None

    def __init__(self):
        self.host = os.environ.get('CONTIFLOW_HOST')
        self.project = os.environ.get('CONTIFLOW_PROJECT')
        self.job = os.environ.get('CONTIFLOW_JOB')
        self.step = os.environ.get('CONTIFLOW_STEP')

    def getBaseUrl(self):
        return self.host + "/api"

    def getProject(self):
        return self.project
    
    def getJob(self):
        return self.job

    def getStep(self):
        return self.step


