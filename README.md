# Read Me

## Requirements

- Python >= 3.7



## PyClientLib

### Client

The class client can be created with either of two functions, "from_env" and "init_with".

```python
class Client:
    env: Environment # the env stores valuable informations ,like the host adress and the running jobs

    Workers: WorkerCollection # Workers helps to manage the workers of the client
    Projects: ProjectCollection # Projects are there to manage the projects of the client
    Jobs: JobCollection # Jobs help to manage the jobs of the client
    Scheduler: Scheduler # Scheduler helps to manage the Sschedluer of the client
    Fragments: FragmentCollection # Fragments help to manage the fragments of the client

```

#### from_env

The "from_env" creates an object of the type client with informations that are saved in the environment.

```python
client = mlcycle.from_env()
```

#### init_with

The method "init_with" creates an object of the class client with the host address.

```python
host = "https://192.168.99.100:5001/api" # backend address

client = mlcycle.init_with(host)
```





### JobCollection

Below is an example of the dataclass job, as it is a return value in every method in the JobCollection Class


```python
Job(
    initiator=0, #0=Manual;1=Git;2=Data
    state=21, #0=Created;1=InProgress;2=Done;21=Scheduled;31=Error
    steps=[
        Step(
            name='Bootstrap',
            number=0,
            state=21, #0=Created;1=InProgress;2=Done;21=Scheduled;31=Error
            start='2019-08-15T09:10:52.589Z',
            end='2019-08-15T09:10:55.359Z',
            docker=None,
            metrics=None,
            fragments=[
                Fragment(
                    created='2019-08-15T09:10:55.069Z',
                    filename='0_console.log',
                    type=1, #0=Metrics;1=BuildLogs;2=Model
                    name='Console Log',
                    step_number=None, 
                    job_id=None,
                    id='9c3e1857-003c-4885-8b87-8d180335e6d9'
                )],
            id=None
        ),
        
        ... # more steps
        
        Step(
                name='Train', 
                number=3,
                state=1, 
                start='2019-08-16T08:35:22.774Z', 
                end=None, 
                docker=DockerConfiguration(
                    command='python train/train.py',
                    image=None, 
                    build_configuration=DockerBuildConfiguration(
                        context='train/', 
                        dockerfile='dockerfile', 
                        properties=None), 
                    properties=None), 
                metrics={'Loss': 0.11768476468261843, 'Accuracy': 0.9822}
                fragments=None, 
                id=None
            ),
        
        ... # more steps
        
    ],
    project=Project(
        name='Project 1',
        git_repository='https://github.com/cemizm/tf-benchmark-gpu.git',
        id='97df69fb-8fe1-48a1-835f-c0d699789a78'),
    project_id=None,
    created='2019-08-15T09:10:52.424Z',
    finished='2019-08-15T09:10:55.359Z',
    id='e0578355-2532-4363-a15c-7753cd5ed987'
)
```

#### get all

The "get_all" method returns a list of Jobs like you can see above. It will leave out the fragments

```python
return_value = client.Jobs.get_all()
```

#### get by id

The "get_by_id" method returns a single step with every information available(like you can see above)


```python
job_id = "e0578355-2532-4363-a15c-7753cd5ed987"

return_value = client.Jobs.get_by_id(job_id)
```

#### add steps

The "add_steps" method adds one or more steps to a job. It returns the job like you can see above


```python
job_id = "e0578355-2532-4363-a15c-7753cd5ed987"
steps = [
    Step(
        name='Train', 
        number=6, 
        state=1, #0=Created;1=InProgress;2=Done;21=Scheduled;31=Error
        start=None, 
        end=None, 
        docker=DockerConfiguration(
            command='python train/train.py', 
            image=None, 
            build_configuration=None,
            properties=None), 
        metrics=None, 
        fragments=None, 
        id=None
    )]
  
return_value = client.Jobs.add_steps(job_id, steps)
```

#### add metrics

You can use the method "add_metrics" to add metrics as a dictionary to the individual steps. The metrics are added to a running step of a job and must also be passed.

```python
metrics = {'Loss': 0.11768476468261843, 'Accuracy': 0.9822}
job_id = e0578355-2532-4363-a15c-7753cd5ed987
step_number = 3
  
return_value = client.Jobs.add_metrics(metrics, job_id, step_number)
```

#### trigger

You start a new job of a project. To do this, pass the appropriate ID of the project to the "trigger" method.


```python
project_id='903778ca-5ed8-4b25-8cf8-6e87a83e581a'
return_value = client.Jobs.trigger(project_id)
```

```python
return_value
-------------------
Job(
    initiator=0, #0=Manual;1=Git;2=Data
    state=1, #0=Created;1=InProgress;2=Done;21=Scheduled;31=Error
    steps=[
        Step(
            name='Bootstrap', 
            number=0, 
            state=21, #0=Created;1=InProgress;2=Done;21=Scheduled;31=Error
        )],
    project_id='903778ca-5ed8-4b25-8cf8-6e87a83e581a',
    created='2019-08-15T11:52:21.2096575+00:00',
    id='ce83f9f1-cb19-4059-96c6-020291a54c6e'
)
```





### Scheduler

The Scheduler can use the "get_pending" method to find out which jobs or their steps are still open. With the method "claim" a step will be assigned and at the end you can finish the step with the methods "complete" or "error".

#### get pending

The "get_pending" method gets all pending jobs and returns them in a list like in the example below.

```python
return_value = client.Scheduler.get_pending()
```

```python
[
    Job(
        initiator=0, 
        steps=[
            Step(
                name='Bootstrap', 
                number=0,
            )
        ],
        project_id='9bb9d33c-108b-4592-a87c-1b2fccbc8004', 
        created='2019-08-08T06:43:09.317Z',
        id='7bbd354f-931b-43aa-acba-f9ff1e7cda6d'
    )
]
```

#### claim

With the method "claim" you can claim a step of a job. It returns a boolean, True on success and False otherwise.

```python
job_id = '7bbd354f-931b-43aa-acba-f9ff1e7cda6d'
step_number = 0

return_value = client.Scheduler.claim(job_id, step_number)
```

#### complete

The method "complete" is used to show that a step is completed. It returns a boolean, True on success and False otherwise.

```python
job_id = '7bbd354f-931b-43aa-acba-f9ff1e7cda6d'
step_number = 0

return_value = client.Scheduler.complete(job_id, step_number)
```

#### error

The method "error" is used to show that a step resulted into an error. It returns a boolean, True on success and False otherwise.

```python
job_id = '7bbd354f-931b-43aa-acba-f9ff1e7cda6d'
step_number = 0

return_value = client.Scheduler.claim(job_id, step_number)
```





### FragmentCollection

The Fragment class is used to download and upload files from steps.

``` python
Fragment(
    created='2019-08-22T15:28:13.759Z',
    filename='0_console.log',
    type=1, #0=Metrics;1=BuildLogs;2=Model
    name='Console Log',
    step_number=0,
    job_id='988dc298-b5cf-4505-ae91-42495dab65e7',
    id='8db16292-c0cf-4def-8e64-d282d974f1a5'
)
```

#### get all by job

the method "get_all_by_job" returns a list of every fragment of the job with the passed id , like in the format you can see in the example above.

```python
job_id = '7bbd354f-931b-43aa-acba-f9ff1e7cda6d'

return_value = client.Fragments.get_all_by_job(job_id)
```

#### get all by step

the method "get_all_by_step" returns a list of every fragment of the job with the passed id and the specified stepnumber, in the format you can see in the example above.

```python
job_id = '7bbd354f-931b-43aa-acba-f9ff1e7cda6d'
step_number = 0

return_value = client.Fragments.get_all_by_step(job_id, step_number)
```

#### get latest by job

the method "get_latest_by_job" downloads a fragment of the specified(latest on default) job. You need to pass a filehandler in writebyte mode and the filename of the fragment. It returns True on success and False otherwise.

```python
fragmentname = "console.log"
handle = open('filename', 'wb')
job_id = '7bbd354f-931b-43aa-acba-f9ff1e7cda6d'

return_value = client.Fragments.get_latest_by_job(fragmentname, handle, job_id)
```

#### get latest by project

the method "get_latest_by_project" downloads a fragment of the specified(latest on default) project. You need to pass a filehandler in writebyte mode and the filename of the fragment. It returns True on success and False otherwise.

```python
fragmentname = "console.log"
handle = open('filename', 'wb')
project_id = '9bb9d33c-108b-4592-a87c-1b2fccbc8004'

return_value = client.Fragments.get_latest_by_project(fragmentname, handle, project_id)
```

#### get by id

the method "get_by_id" downloads the fragment with the specified id. You need to pass a filehandler in writebyte mode. It returns True on success and False otherwise.

```python
handle = open('filename', 'wb')
fragment_id = '8db16292-c0cf-4def-8e64-d282d974f1a5'

return_value = client.Fragments.get_by_id(fragment_id, handle)
```

#### upload

the method "upload" uploads a fragment to a specified step of a job. You need to pass a filehandler in read mode, a fragment to upload and the job_id and stepnumber as destination. It returns the uploaded Fragment on success and False otherwise.

```python
fragment = 
    Fragment(
        filename='0_console.log',
        type=1, #0=Metrics;1=BuildLogs;2=Model
        name='Console Log'
    )
handle = open('filename', 'r')
job_id = '7bbd354f-931b-43aa-acba-f9ff1e7cda6d'
stepnumber = 0

return_value = client.Fragments.upload(fragment, handle, job_id, stepnumber)
```





### ProjectCollection

The ProjectCollection contains methods to manage you projects.

Below is an example of the dataclass Project, as it is a return value in most methods in the ProjectCollection Class. Every method of this class returns false if the request was not successful and they raise an ApiError if the parameters are in a wrong format.

```python
Project(
    name='Project 1',
    git_repository='https://github.com/cemizm/tf-benchmark-gpu.git',
    id='97df69fb-8fe1-48a1-835f-c0d699789a78'
)
```

#### get all

The "get_all" method returns a list of Projects like you can see above. 

```python
return_value = client.Projects.get_all()
```

#### get by id

The "get_by_id" method returns the Project with the according id in the format you can see above. 

```python
project_id = "97df69fb-8fe1-48a1-835f-c0d699789a78"

return_value = client.Projects.get_by_id(project_id)
```

#### add

The "add" method adds a Project. The Project you add has to be a instance of the dataclass project. The method returns the added project on success.

```python
project = 
    Project(
        name='new Project',
        git_repository='https://github.com/cemizm/tf-benchmark-gpu.git'
    )

return_value = client.Projects.add(project)
```

#### update

The "update" method updates a existing Project.  You have to specify the project you want to change with the id. The content you want to change, you hand over as a new project. On success the method returns the updated project.

```python
project_id = "97df69fb-8fe1-48a1-835f-c0d699789a78"
project = 
    Project(
        name='updated Project',
        git_repository='https://github.com/cemizm/tf-benchmark-gpu.git'
    )

return_value = client.Projects.update(project_id, project)
```

#### delete

The "delete" method deletes the project with the specified project_id. It returns True on success, False otherwise.

```python
project_id = "97df69fb-8fe1-48a1-835f-c0d699789a78"

return_value = client.Projects.delete(project_id)
```





### WorkerCollection

The WorkerCollection contains methods to manage you workers.

Below is an example of the dataclass Worker, as it is a return value in most methods in the WorkerCollection Class. Every method of this class returns false if the request was not successful and they raise an ApiError if the parameters are in a wrong format.

```python
Worker(
    name='Worker 1',
    id='4efab54c-1571-480f-b4dc-d7c00948b7f8'
)
```

#### get all

The "get_all" method returns a list of Workers like you can see above. 

```python
return_value = client.Workers.get_all()
```

#### get by id

The "get_by_id" method returns the Worker with the according id in the format you can see above. 

```python
worker_id = "97df69fb-8fe1-48a1-835f-c0d699789a78"

return_value = client.Workers.get_by_id(worker_id)
```

#### add

The "add" method adds a Worker. The Worker you add has to be a instance of the dataclass Worker. The method returns the added Worker on success.

```python
worker = 
    Worker(
        name='new Worker'
	)

return_value = client.Workers.add(worker)
```

#### update

The "update" method updates a existing Worker.  You have to specify the Worker you want to change with the id. The content you want to change, you hand over as a new Worker. On success the method returns the updated Worker.

```python
worker_id = "97df69fb-8fe1-48a1-835f-c0d699789a78"
worker = 
    Worker(
        name='updated worker'
	)

return_value = client.Workers.update(worker_id, worker)
```

#### delete

The "delete" method deletes the Worker with the specified worker_id. It returns True on success, False otherwise.

```python
worker_id = "97df69fb-8fe1-48a1-835f-c0d699789a78"

return_value = client.Workers.delete(worker_id)
```





## Testing
### Requirements

- httmock latest version



### Quick Start

1. Change directory to test
2. Execute tests

```shell
cd test
# if you don´t specify a file it will discover every test file and execute it
# -v shows more detail
python -m unittest -v
```

### Options

- ```-m unittest``` starts the unittests
- ``` -v ``` shows more details
- if no file is specified, it will discover every unittest and them

