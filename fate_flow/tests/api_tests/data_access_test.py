import time
import unittest

import requests
from fate_flow.settings import HTTP_PORT, API_VERSION, WORK_MODE


class TestDataAccess(unittest.TestCase):
    def setUp(self):
        self.upload_guest_config = {"file": "examples/data/breast_b.csv", "head": 1, "partition": 10, "work_mode": WORK_MODE, "namespace": "fate_flow_unittest_breast", "table_name": "breast_b", "use_local_data": 0, 'drop': 0}
        self.upload_host_config = {"file": "examples/data/breast_a.csv", "head": 1, "partition": 10, "work_mode": WORK_MODE, "namespace": "fate_flow_unittest_breast", "table_name": "breast_b", "use_local_data": 0, 'drop': 0}
        self.download_config = {"output_path": "./fate_flow_unittest_breast_b.csv", "work_mode": WORK_MODE,
                                "namespace": "fate_flow_unittest_breast", "table_name": "breast_b"}
        self.server_url = "http://{}:{}/{}".format('127.0.0.1', HTTP_PORT, API_VERSION)

    def test_upload_guest(self):
        response = requests.post("/".join([self.server_url, 'data', 'upload']), json=self.upload_guest_config)
        self.assertTrue(response.status_code in [200, 201])
        self.assertTrue(int(response.json()['retcode']) == 0)
        job_id = response.json()['jobId']
        for i in range(60):
            response = requests.post("/".join([self.server_url, 'job', 'query']), json={'job_id': job_id})
            self.assertTrue(int(response.json()['retcode']) == 0)
            if response.json()['data'][0]['f_status'] == 'success':
                break
            time.sleep(1)

    def test_upload_host(self):
        response = requests.post("/".join([self.server_url, 'data', 'upload']), json=self.upload_host_config)
        self.assertTrue(response.status_code in [200, 201])
        self.assertTrue(int(response.json()['retcode']) == 0)
        job_id = response.json()['jobId']
        for i in range(60):
            response = requests.post("/".join([self.server_url, 'job', 'query']), json={'job_id': job_id})
            self.assertTrue(int(response.json()['retcode']) == 0)
            if response.json()['data'][0]['f_status'] == 'success':
                break
            time.sleep(1)

    def test_upload_history(self):
        response = requests.post("/".join([self.server_url, 'data', 'upload/history']), json={'limit': 2})
        self.assertTrue(response.status_code in [200, 201])
        self.assertTrue(int(response.json()['retcode']) == 0)

    def test_download(self):
        response = requests.post("/".join([self.server_url, 'data', 'download']), json=self.download_config)
        self.assertTrue(response.status_code in [200, 201])
        self.assertTrue(int(response.json()['retcode']) == 0)


if __name__ == '__main__':
    unittest.main()


