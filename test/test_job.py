import mlcycle
import dataclasses
import unittest

from httmock import all_requests, HTTMock


@all_requests
def get_all(url, request):
    return {'status_code': 200,'content': '[{"id": "e0578355-2532-4363-a15c-7753cd5ed987","created": "2019-08-15T09:10:52.424Z","finished": "2019-08-15T09:10:55.359Z","state": 31,"initiator": 0,"project": {"name": "Project 1","gitRepository": "https://github.com/cemizm/tf-benchmark-gpu.git","id": "97df69fb-8fe1-48a1-835f-c0d699789a78"},"steps": [{"name": "Bootstrap","number": 0,"start": "2019-08-15T09:10:52.589Z","end": "2019-08-15T09:10:55.359Z","state": 31}]}]'}

@all_requests
def get_by_id(url, request):
    return {'status_code': 200,'content': '{"id": "e0578355-2532-4363-a15c-7753cd5ed987","created": "2019-08-15T09:10:52.424Z","finished": "2019-08-15T09:10:55.359Z","state": 31,"initiator": 0,"project": {"name": "Project 1","gitRepository": "https://github.com/cemizm/tf-benchmark-gpu.git","id": "97df69fb-8fe1-48a1-835f-c0d699789a78"},"steps": [{"name": "Bootstrap","number": 0,"start": "2019-08-15T09:10:52.589Z","end": "2019-08-15T09:10:55.359Z","state": 31,"fragments": [{"id": "9c3e1857-003c-4885-8b87-8d180335e6d9","created": "2019-08-15T09:10:55.069Z","name": "Console Log","filename": "0_console.log","type": 1}]}]}'}


@all_requests
def add_steps(url, request):
    return {'status_code': 200,'content': '{"projectId": "903778ca-5ed8-4b25-8cf8-6e87a83e581a", "created": "2019-08-16T08:35:17.574Z", "initiator": 0, "state": 1, "steps": [{"number": 0, "name": "Bootstrap", "state": 2, "start": "2019-08-16T08:35:17.605Z", "end": "2019-08-16T08:35:19.173Z"}, {"number": 1, "name": "Ingest", "state": 2, "start": "2019-08-16T08:35:19.216Z", "end": "2019-08-16T08:35:20.979Z", "docker": {"image": "python:3", "command": "python ingest.py"}}, {"number": 2, "name": "Prepare", "state": 2, "start": "2019-08-16T08:35:21.034Z", "end": "2019-08-16T08:35:22.724Z", "docker": {"image": "python:3", "command": "python prepare.py"}}, {"number": 3, "name": "Train", "state": 1, "start": "2019-08-16T08:35:22.774Z", "docker": {"buildConfiguration": {"context": "train/", "dockerfile": "dockerfile"}, "command": "python train/train.py"}}, {"number": 4, "name": "Validate", "state": 0, "docker": {"image": "python:3", "command": "python validate.py"}}, {"number": 5, "name": "Train", "state": 0, "docker": {"command": "python train/train.py"}}, {"number": 6, "name": "Train", "state": 0, "docker": {"command": "python train/train.py"}}], "id": "1dc38c43-705b-4100-8f47-2146c69f472c"}'}

@all_requests
def add_metrics(url, request):
    return {'status_code': 200,'content': '{"projectId": "903778ca-5ed8-4b25-8cf8-6e87a83e581a", "created": "2019-08-16T08:35:17.574Z", "initiator": 0, "state": 1, "steps": [{"number": 0, "name": "Bootstrap", "state": 2, "start": "2019-08-16T08:35:17.605Z", "end": "2019-08-16T08:35:19.173Z"}, {"number": 1, "name": "Ingest", "state": 2, "start": "2019-08-16T08:35:19.216Z", "end": "2019-08-16T08:35:20.979Z", "docker": {"image": "python:3", "command": "python ingest.py"}}, {"number": 2, "name": "Prepare", "state": 2, "start": "2019-08-16T08:35:21.034Z", "end": "2019-08-16T08:35:22.724Z", "docker": {"image": "python:3", "command": "python prepare.py"}}, {"number": 3, "name": "Train", "state": 1, "start": "2019-08-16T08:35:22.774Z", "docker": {"buildConfiguration": {"context": "train/", "dockerfile": "dockerfile"}, "command": "python train/train.py"}, "metrics": {"Loss": 0.11768476468261843, "Accuracy": 0.9822}}, {"number": 4, "name": "Validate", "state": 0, "docker": {"image": "python:3", "command": "python validate.py"}}, {"number": 5, "name": "Train", "state": 0, "docker": {"command": "python train/train.py"}}, {"number": 6, "name": "Train", "state": 0, "docker": {"command": "python train/train.py"}}], "id": "1dc38c43-705b-4100-8f47-2146c69f472c"}'}

@all_requests
def trigger(url, request):
    return {'status_code': 200,'content': '{"projectId": "903778ca-5ed8-4b25-8cf8-6e87a83e581a","created": "2019-08-15T11:52:21.2096575+00:00","initiator": 0,"state": 0,"steps": [{"number": 0,"name": "Bootstrap","state": 21}],"id": "ce83f9f1-cb19-4059-96c6-020291a54c6e"}'}


class TestJob(unittest.TestCase):
    def setUp(self):
        self.client = mlcycle.init_with("https://192.168.99.100:5001/api")

    def test_get_all(self):
        with HTTMock(get_all):
            job = mlcycle.models.Job(id="e0578355-2532-4363-a15c-7753cd5ed987",
                created="2019-08-15T09:10:52.424Z",
                finished="2019-08-15T09:10:55.359Z", state=31, initiator=0,
                project=mlcycle.models.Project(name="Project 1",
                gitRepository="https://github.com/cemizm/tf-benchmark-gpu.git",
                id="97df69fb-8fe1-48a1-835f-c0d699789a78"),
                steps=[mlcycle.models.Step(name="Bootstrap",
                number=0, start="2019-08-15T09:10:52.589Z",
                end="2019-08-15T09:10:55.359Z", state=31)])
            resp = self.client.Jobs.get_all()
            self.assertTrue(dataclasses.is_dataclass(resp[0]))
            self.assertEqual(resp[0], job)

    def test_get_by_id(self):
        with HTTMock(get_by_id):
            job = mlcycle.models.Job(id="e0578355-2532-4363-a15c-7753cd5ed987",
                created="2019-08-15T09:10:52.424Z",
                finished="2019-08-15T09:10:55.359Z", state=31, initiator=0,
                project=mlcycle.models.Project(name="Project 1",
                gitRepository="https://github.com/cemizm/tf-benchmark-gpu.git",
                id="97df69fb-8fe1-48a1-835f-c0d699789a78"),
                steps=[mlcycle.models.Step(name="Bootstrap",
                number=0, start="2019-08-15T09:10:52.589Z",
                end="2019-08-15T09:10:55.359Z", state=31,fragments=[mlcycle.models.Fragment(
                id="9c3e1857-003c-4885-8b87-8d180335e6d9", created="2019-08-15T09:10:55.069Z",
                name="Console Log",filename="0_console.log",type=1)])])
            resp = self.client.Jobs.get_by_id(job.id)
            self.assertTrue(dataclasses.is_dataclass(resp))
            self.assertEqual(resp, job)

    def test_add_steps(self):
        with HTTMock(add_steps):
            job = mlcycle.models.Job(projectId='903778ca-5ed8-4b25-8cf8-6e87a83e581a', 
                created='2019-08-16T08:35:17.574Z', initiator=0, state=1,steps=[
                mlcycle.models.Step(number=0, name='Bootstrap',
                state=2, start='2019-08-16T08:35:17.605Z',
                end='2019-08-16T08:35:19.173Z'),
                mlcycle.models.Step(number=1, name='Ingest',state=2,
                start='2019-08-16T08:35:19.216Z', end='2019-08-16T08:35:20.979Z',
                docker=mlcycle.models.DockerConfiguration(image='python:3',
                command='python ingest.py')),
                mlcycle.models.Step(number=2,name='Prepare',state=2,
                start='2019-08-16T08:35:21.034Z',end='2019-08-16T08:35:22.724Z',
                docker=mlcycle.models.DockerConfiguration(image='python:3',
                command='python prepare.py')),
                mlcycle.models.Step(number=3,name='Train',
                state=1, start='2019-08-16T08:35:22.774Z',
                docker=mlcycle.models.DockerConfiguration(
                buildConfiguration=mlcycle.models.DockerBuildConfiguration(context='train/',
                dockerfile='dockerfile'), command='python train/train.py')),
                mlcycle.models.Step(number=4, name='Validate',state=0,
                docker=mlcycle.models.DockerConfiguration(image='python:3',
                command='python validate.py')),
                mlcycle.models.Step(number=5,name='Train',
                state=0, docker=mlcycle.models.DockerConfiguration(
                command='python train/train.py')),
                mlcycle.models.Step(number=6,
                name='Train',state=0, docker=mlcycle.models.DockerConfiguration(
                command='python train/train.py'))],
                id='1dc38c43-705b-4100-8f47-2146c69f472c')
                
            steps=[job.steps[1],job.steps[2],job.steps[3],job.steps[4]]
            resp = self.client.Jobs.add_steps(job.id, steps)
            self.assertTrue(dataclasses.is_dataclass(resp))
            self.assertEqual(resp, job)

    def test_add_metrics(self):
        with HTTMock(add_metrics):
            metrics={"Loss": 0.11768476468261843, "Accuracy": 0.9822}
            job = mlcycle.models.Job(projectId='903778ca-5ed8-4b25-8cf8-6e87a83e581a', 
                created='2019-08-16T08:35:17.574Z', initiator=0, state=1,steps=[
                mlcycle.models.Step(number=0, name='Bootstrap',
                state=2, start='2019-08-16T08:35:17.605Z',
                end='2019-08-16T08:35:19.173Z'),
                mlcycle.models.Step(number=1, name='Ingest',state=2,
                start='2019-08-16T08:35:19.216Z', end='2019-08-16T08:35:20.979Z',
                docker=mlcycle.models.DockerConfiguration(image='python:3',
                command='python ingest.py')),
                mlcycle.models.Step(number=2,name='Prepare',state=2,
                start='2019-08-16T08:35:21.034Z',end='2019-08-16T08:35:22.724Z',
                docker=mlcycle.models.DockerConfiguration(image='python:3',
                command='python prepare.py')),
                mlcycle.models.Step(number=3,name='Train',
                state=1, start='2019-08-16T08:35:22.774Z',
                docker=mlcycle.models.DockerConfiguration(
                buildConfiguration=mlcycle.models.DockerBuildConfiguration(context='train/',
                dockerfile='dockerfile'), command='python train/train.py'),
                metrics=metrics),
                mlcycle.models.Step(number=4, name='Validate',state=0,
                docker=mlcycle.models.DockerConfiguration(image='python:3',
                command='python validate.py')),
                mlcycle.models.Step(number=5,name='Train',
                state=0, docker=mlcycle.models.DockerConfiguration(
                command='python train/train.py')),
                mlcycle.models.Step(number=6,
                name='Train',state=0, docker=mlcycle.models.DockerConfiguration(
                command='python train/train.py'))],
                id='1dc38c43-705b-4100-8f47-2146c69f472c')
                
            resp = self.client.Jobs.add_metrics(metrics, job.id, 3)
            self.assertTrue(dataclasses.is_dataclass(resp))
            self.assertEqual(resp, job)

    def test_trigger(self):
        with HTTMock(trigger):
            job = mlcycle.models.Job(projectId="903778ca-5ed8-4b25-8cf8-6e87a83e581a",
                created="2019-08-15T11:52:21.2096575+00:00", initiator=0, state=0,
                steps=[mlcycle.models.Step(number=0,name="Bootstrap",state=21)],
                id="ce83f9f1-cb19-4059-96c6-020291a54c6e")
            resp = self.client.Jobs.trigger(job.project_id)
            self.assertTrue(dataclasses.is_dataclass(resp))
            self.assertEqual(resp, job)


if __name__ == '__main__':
    unittest.main()