import mlcycle
import dataclasses
import unittest
import json
import uuid

from httmock import all_requests, HTTMock

@all_requests
def get_pending_success(url, request):
    return {'status_code': 200,
        'content': '[{"projectId": "9bb9d33c-108b-4592-a87c-1b2fccbc8004","jobId": "7bbd354f-931b-43aa-acba-f9ff1e7cda6d","created":"2019-08-08T06:43:09.317Z","initiator": 0,"step":{"number": 0,"name": "Bootstrap"}}]'}

@all_requests
def get_pending_200_bad_content(url, request):
    return {'status_code': 200,
        'content': 'something might be wrong with this json'}

@all_requests
def get_pending_400(url, request):
    return {'status_code': 400,
        'content': '[{"projectId": "9bb9d33c-108b-4592-a87c-1b2fccbc8004","jobId": "7bbd354f-931b-43aa-acba-f9ff1e7cda6d","created":"2019-08-08T06:43:09.317Z","initiator": 0,"step":{"number": 0,"name": "Bootstrap"}}]'}

@all_requests
def claim_success(url, request):
    return {'status_code': 200}

@all_requests
def claim_not_scheduled(url, request):
    return {'status_code': 406, 'content': "Step is not scheduled"}
 
@all_requests
def complete_success(url, request):
    return {'status_code': 200}

@all_requests
def complete_not_scheduled(url, request):
    return {'status_code': 406, 'content': "Step is not in progress"}
  
@all_requests
def error_success(url, request):
    return {'status_code': 200}

@all_requests
def error_not_scheduled(url, request):
    return {'status_code': 406, 'content': "Step is not in progress"}
 

class TestScheduler(unittest.TestCase):

    def setUp(self):
        self.client = mlcycle.init_with("https://192.168.99.100:5001/api")

    def test_get_pending_success(self):
        with HTTMock(get_pending_success):
            resp = self.client.Scheduler.get_pending()
            pending = mlcycle.models.Job(initiator=0, state=None,
                steps=[mlcycle.models.Step(name='Bootstrap', number=0,
                state=None, start=None, end=None, docker=None, metrics=None,
                fragments=None, id=None)], project=None,
                projectId='9bb9d33c-108b-4592-a87c-1b2fccbc8004',
                created='2019-08-08T06:43:09.317Z', finished=None,
                id='7bbd354f-931b-43aa-acba-f9ff1e7cda6d')
            self.assertTrue(dataclasses.is_dataclass(resp[0]))
            self.assertTrue(dataclasses.is_dataclass(resp[0].steps[0]))
            self.assertEqual(resp[0], pending)

    def test_get_pending_200_bad_content(self):
        with HTTMock(get_pending_200_bad_content):
            with self.assertRaises(json.decoder.JSONDecodeError):
                self.client.Scheduler.get_pending()

    def test_get_pending_400(self):
        with HTTMock(get_pending_400):
            resp = self.client.Scheduler.get_pending()
            self.assertFalse(resp)

    def test_claim_success(self):
        with HTTMock(claim_success):
            job_id = "7bbd354f-931b-43aa-acba-f9ff1e7cda6d"
            resp = self.client.Scheduler.claim(job_id, 2)
            self.assertTrue(resp)

    def test_claim_empty_jobid(self):
        with HTTMock(claim_success):
            with self.assertRaises(mlcycle.apierror.ApiError):
                job_id = ""
                self.client.Scheduler.claim(job_id, 2)

    def test_claim_empty_step(self):
            with self.assertRaises(mlcycle.apierror.ApiError):
                job_id = "7bbd354f-931b-43aa-acba-f9ff1e7cda6d"
                self.client.Scheduler.claim(job_id, "")

    def test_claim_not_scheduled(self):
        with HTTMock(claim_not_scheduled):
            job_id = "7bbd354f-931b-43aa-acba-f9ff1e7cda6d"
            resp = self.client.Scheduler.claim(job_id, 2)
            self.assertFalse(resp)
    
    def test_complete_success(self):
        with HTTMock(complete_success):
            job_id = "7bbd354f-931b-43aa-acba-f9ff1e7cda6d"
            resp = self.client.Scheduler.complete(job_id, 2)
            self.assertTrue(resp)

    def test_complete_empty_jobid(self):
        with HTTMock(complete_success):
            with self.assertRaises(mlcycle.apierror.ApiError):
                job_id = ""
                self.client.Scheduler.complete(job_id, 2)

    def test_complete_empty_step(self):
        with HTTMock(complete_success):
            with self.assertRaises(mlcycle.apierror.ApiError):
                job_id = "7bbd354f-931b-43aa-acba-f9ff1e7cda6d"
                self.client.Scheduler.complete(job_id, "")

    def test_complete_not_scheduled(self):
        with HTTMock(complete_not_scheduled):
            job_id = "7bbd354f-931b-43aa-acba-f9ff1e7cda6d"
            resp = self.client.Scheduler.complete(job_id, 2)
            self.assertFalse(resp)

    def test_error_success(self):
        with HTTMock(error_success):
            job_id = "7bbd354f-931b-43aa-acba-f9ff1e7cda6d"
            resp = self.client.Scheduler.error(job_id, 2)
            self.assertTrue(resp)

    def test_error_empty_jobid(self):
        with HTTMock(error_success):
            with self.assertRaises(mlcycle.apierror.ApiError):
                job_id = ""
                self.client.Scheduler.error(job_id, 2)

    def test_error_empty_step(self):
        with HTTMock(error_success):
            with self.assertRaises(mlcycle.apierror.ApiError):
                job_id = "7bbd354f-931b-43aa-acba-f9ff1e7cda6d"
                self.client.Scheduler.error(job_id, "")

    def test_error_not_scheduled(self):
        with HTTMock(error_not_scheduled):
            job_id = "7bbd354f-931b-43aa-acba-f9ff1e7cda6d"
            resp = self.client.Scheduler.error(job_id, 2)
            self.assertFalse(resp)

    def test_check_success(self):
        job_id = "7bbd354f-931b-43aa-acba-f9ff1e7cda6d"
        self.client.Scheduler.check(job_id, 2)
        self.assertTrue(True)

    def test_check_empty_jobid(self):
        job_id = ""
        with self.assertRaises(mlcycle.apierror.ApiError):
            self.client.Scheduler.check(job_id, 2)

    def test_check_jobid_not_uuid(self):
        job_id = "not a valid uuid"
        with self.assertRaises(mlcycle.apierror.ApiError):
            self.client.Scheduler.check(job_id, 2)

    def test_check_empty_step(self):
        job_id = "7bbd354f-931b-43aa-acba-f9ff1e7cda6d"
        with self.assertRaises(mlcycle.apierror.ApiError):
            self.client.Scheduler.check(job_id, "")

    def test_check_step_bad_string(self):
        job_id = "7bbd354f-931b-43aa-acba-f9ff1e7cda6d"
        with self.assertRaises(mlcycle.apierror.ApiError):
            self.client.Scheduler.check(job_id, "this is not an int")

    def test_check_step_float(self):
        job_id = "7bbd354f-931b-43aa-acba-f9ff1e7cda6d"
        with self.assertRaises(mlcycle.apierror.ApiError):
            self.client.Scheduler.check(job_id, 2.0)

    def test_check_step_int_string(self):
        job_id = "7bbd354f-931b-43aa-acba-f9ff1e7cda6d"
        self.client.Scheduler.check(job_id, "2")
        self.assertTrue(True)

    def test_check_step_negative(self):
        job_id = "7bbd354f-931b-43aa-acba-f9ff1e7cda6d"
        with self.assertRaises(mlcycle.apierror.ApiError):
            self.client.Scheduler.check(job_id, -2)


if __name__ == '__main__':
    unittest.main()