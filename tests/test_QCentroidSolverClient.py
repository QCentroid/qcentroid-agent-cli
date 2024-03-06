import responses
import requests
from qcentroid_agent_cli import QCentroidSolverClient
from json import dumps

API_BASE_URL="https://api.qcentroid.xyz"
SOLVER_API_KEY="1234-4567-8910"  # Get your solver API_KEY in the platform dashboard
SOLVER_ID="123"
base_url=API_BASE_URL
requested_url = f"{base_url}/agent/solver/{SOLVER_ID}/webhook"
requested_ok_response = {'id': 1, 'name': 'JSQO4I5NJNER', 'started_at': '2024-02-29T01:16:10', 'end_at': '2024-02-29T01:16:17', 'status': 'PENDING', 'details': None, 'user_id': 1, 'problem_id': 1, 'data': {}, 'num_shots': 1, 'data_file_id': 1, 'solver_rank': None, 'description': None, 'comment': '', 'tag': None, 'organization_id': 1, 'attributes': None, 'token': 'token'}
requested_no_response = {}
solver = QCentroidSolverClient(API_BASE_URL, SOLVER_API_KEY, SOLVER_ID)

def test_found_job():
    @responses.activate
    def run():
        
        responses.add(responses.GET, requested_url,
                  json=requested_ok_response,
                  status=200)

        job = solver.obtainJob()

        assert job is not None

        assert responses.calls[0].request.url == requested_url
        assert responses.calls[0].response.text == dumps(requested_ok_response)
    run()
    
def test_job_not_found():
    @responses.activate
    def run():
        responses.add(responses.GET, requested_url,
                  json=requested_no_response,
                  status=204)
        
        job = solver.obtainJob()

        assert job is None
        assert responses.calls[0].request.url == requested_url
        assert responses.calls[0].response.text == dumps(requested_no_response)
