class Environment:
    """Environmente

    Attributes:
        host: base url for requests
        project: current project
        job: current job
        step: current step

    """
    host = None
    project = None
    job = None
    step = None

    def __init__(self, host, project=None, job=None, step=None):
        self.host = host
        self.project = project
        self.job = job
        self.step = step

    def get_base_url(self):
        return self.host

    def get_project(self):
        return self.project

    def get_job(self):
        return self.job

    def get_step(self):
        return self.step
