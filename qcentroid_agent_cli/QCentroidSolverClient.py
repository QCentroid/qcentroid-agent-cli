import requests
import json
import os
import mimetypes
from qcentroid_agent_cli.model import StatusEntity
from qcentroid_agent_cli import QCentroidAgentClient

import ssl

api_base_url = "https://api.qcentroid.xyz"

class QCentroidSolverClient:
    # Init class with base parameters
    def __init__(self, base_url=None, api_key=None, solver_id=None):
        self.base_url = api_base_url #default production url
        
        if base_url is not None:
            self.base_url = base_url
        else:
            self.base_url = os.environ.get('QCENTROID_PUBLIC_API', api_base_url)
        if api_key is not None:             
            self.api_key = api_key
        else:
            self.api_key = os.environ.get('QCENTROID_AGENT_API_TOKEN')
        if solver_id is not None:             
            self.solver_id = job_name
        else:
            self.solver_id = os.environ.get('QCENTROID_SOLVER_ID')

    def getHeaders(self):
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Accept": "application/json",  # Set the content type based on your API's requirements
            "Content-Type": "application/json",  # Set the content type based on your API's requirements
        }
    #GET [core]/agent/job/{job_name}/data/input
    def obtainJob(self) -> QCentroidAgentClient:
        try:
            response = requests.get(f"{self.base_url}/agent/solver/{self.solver_id}/webhook", headers=self.getHeaders())

            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                # Parse and use the response data as needed
                data = response.json()
                print("API Response:", data)
                return QCentroidAgentClient(self.base_url, data.token, data.job_id) #return  QCentroidAgentClient
            # No jobs
            if response.status_code == 204:                
                return None
            else:
                print(f"Error: {response.status_code} - {response.text}")
                response.raise_for_status()

        except requests.RequestException as e:
            print(f"Request failed: {e}")
            raise e            
        except Exception as e:
            # Handle any exceptions or errors here
            print(f"Unexpected Error: {e}")
            raise e