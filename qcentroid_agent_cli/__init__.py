
import requests
import json
import os
import mimetypes
from io import BytesIO
from qcentroid_agent_cli.model import Status, StatusEntity

import ssl
import logging

api_base_url = "https://api.qcentroid.xyz"

logger = logging.getLogger(__name__)

def processJsonData(response):
    data = {}
    if 'Transfer-Encoding' in response.headers and response.headers['Transfer-Encoding'] == 'chunked':
        datab=b""
        for chunk in response.iter_content(chunk_size=1024):
            datab += chunk                    
        data = json.loads(datab)
    else:
        data = response.json()
    return data

def data2file(data:dict):
    # Serialize the dictionary to JSON
    json_data = json.dumps(data)

    # Encode the JSON string as bytes
    file_content = json_data.encode()

    # Create a file-like object using BytesIO    
    return BytesIO(file_content)

class QCentroidAgentClient:
    # Init class with base parameters
    def __init__(self, base_url=None, pat=None, job_name=None):
        self.base_url = api_base_url #default production url
        
        if base_url is not None:
            self.base_url = base_url
        else:
            self.base_url = os.environ.get('QCENTROID_PUBLIC_API', api_base_url)
        if pat is not None:             
            self.pat = pat
        else:
            self.pat = os.environ.get('QCENTROID_TOKEN')
        if job_name is not None:             
            self.name = job_name
        else:
            self.name = os.environ.get('EXECUTOR_ID')
            
    def getHeaders(self):
        return {
            "Authorization": f"Bearer {self.pat}",
            "Accept": "application/json",  # Set the content type based on your API's requirements
            "Content-Type": "application/json",  # Set the content type based on your API's requirements
        }

    #GET [core]/agent/job/{job_name}/data/input
    def obtainInputData(self) -> dict:        

        try:
            response = requests.get(f"{self.base_url}/agent/job/{self.name}/data/input", headers=self.getHeaders(), stream=True)

            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                # Parse and use the response data as needed                
                data = processJsonData(response)            
                logger.debug(f"API Response:{data}")
                return data #return json 
            else:
                logger.error(f"Error: {response.status_code} - {response.text}")
                response.raise_for_status()

        except requests.RequestException as e:
            logger.error(f"Request failed: {e}", e)
            raise e            
        except Exception as e:
            # Handle any exceptions or errors here
            logger.error(f"Unexpected Error: {e}", e)            
            raise e

    #POST [core]/agent/job/{job_name}/data/output
    def sendOutputData(self, data:dict) -> bool:
        
        file = data2file(data)
        
        try:
            response = requests.post(f"{self.base_url}/agent/job/{self.name}/data/output", json=data, headers=self.getHeaders(), files={"file": file})
            
            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                # Parse and use the response data as needed
                data = processJsonData(response)
                logger.debug(f"API Response:{data}")
                return True
            else:
                logger.error(f"Error: {response.status_code} - {response.text}")
                response.raise_for_status()

        except requests.RequestException as e:
            logger.error(f"Request failed: {e}", e)
            raise e            
        except Exception as e:
            # Handle any exceptions or errors here
            logger.error(f"Unexpected Error: {e}", e)
            raise e
        

    #POST /agent/job/{job_name}/data/output/additional
    def sendAdditionalOutputFile(self, filename:str) -> bool:
        try:
            with open(filename, "rb") as file:
                response = requests.post(f"{self.base_url}/agent/job/{self.name}/data/output/additional", headers=self.getHeaders(), files={"file": file})
                if response.status_code == 200:
                    # Parse and use the response data as needed
                    data = processJsonData(response)
                    logger.debug(f"API Response:{data}")
                    return True
                else:
                    logger.error(f"Error: {response.status_code} - {response.text}")
                    response.raise_for_status()

        except requests.RequestException as e:
            logger.error(f"Request failed: {e}", e)
            raise e            
        except Exception as e:
            # Handle any exceptions or errors here
            logger.error(f"Unexpected Error: {e}", e)
            raise e

    #GET [core]/agent/job/{job}/execution-log
    def sendExecutionLog(self, filename:str) -> bool:
        try:
           
            with open(filename, "rb") as file:
                response = requests.post(f"{self.base_url}/agent/job/{self.name}/execution-log", headers=self.getHeaders(), files={"file": file})
                if response.status_code == 200:
                    # Parse and use the response data as needed
                    data = processJsonData(response)
                    logger.debug(f"API Response:{data}")
                    return True
                else:
                    logger.error(f"Error: {response.status_code} - {response.text}")
                    response.raise_for_status()
                
            
        except FileNotFoundError as e:
            logger.error(f"FileError: {e}", e)
            raise e
        except ValueError as e:
            logger.error(f"Error: {e}", e)
            raise e
        except Exception as e:
            # Handle any other unexpected exceptions here
            logger.error(f"Unexpected Error: {e}", e)
            raise e        
    #GET [core]/agent/job/{job}/status
    def status(self) -> StatusEntity:
        try:
            response = requests.get(f"{self.base_url}/agent/job/{self.name}/status", headers=self.getHeaders())
            
            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                # Parse and use the response data as needed
                data = processJsonData(response)
                logger.debug(f"API Response:{data}")
                current_status = StatusEntity.from_dict(data)
                return current_status
            else:
                logger.error(f"Error: {response.status_code} - {response.text}")
                response.raise_for_status()
        except FileNotFoundError as e:
            logger.error(f"Error: {e}", e)
            raise e
        except ValueError as e:
            logger.error(f"Error: {e}", e)
            raise e
        except Exception as e:
            # Handle any other unexpected exceptions here
            logger.error(f"Unexpected Error: {e}", e)
            raise e

    #POST [core]/agent/job/{job}/status
    def status(self, data:StatusEntity) -> bool:
        try:
            response = requests.post(f"{self.base_url}/agent/job/{self.name}/status", headers=self.getHeaders(), json=data.to_dict())
            if response.status_code == 200:
                # Parse and use the response data as needed
                data = processJsonData(response)
                logger.debug(f"API Response:{data}")
                return True
            else:
                logger.error(f"Error: {response.status_code} - {response.text}")
                response.raise_for_status()

            return response.id
        except FileNotFoundError as e:
            logger.error(f"Error: {e}")
            raise e
        except ValueError as e:
            logger.error(f"Error: {e}")
            raise e
        except Exception as e:
            # Handle any other unexpected exceptions here
            logger.error(f"Unexpected Error: {e}")
            raise e

    def start(self):
        self.status(StatusEntity(Status.RUNNING))
    
    def end(self):
        self.status(StatusEntity(Status.FINISHED))

    def error(self, be:BaseException):        
        self.status(StatusEntity(Status.ERROR))
        self.sendExecutionLog(str(be)) 

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
            self.solver_id = solver_id
        else:
            self.solver_id = os.environ.get('QCENTROID_SOLVER_ID')

    def getHeaders(self):
        return {
            "X-API-Key": self.api_key,
            "Accept": "application/json",  # Set the content type based on your API's requirements
            "Content-Type": "application/json",  # Set the content type based on your API's requirements
        }
    #GET [core]/agent/job/{job_name}/data/input
    def obtainJob(self) -> QCentroidAgentClient:
        try:
            response = requests.get(f"{self.base_url}/agent/solver/{self.solver_id}/webhook", headers=self.getHeaders())

            
            match response.status_code:
                # Check if the request was successful (status code 200)            
                case 200:
                    # Parse and use the response data as needed
                    data = processJsonData(response)
                    logger.info(f"API Response:{data}")
                    return QCentroidAgentClient(self.base_url, data["token"], data["name"]) #return  QCentroidAgentClient
                
                # No jobs
                case 204:                
                    return None
                case _:
                    logger.error(f"Error: {response.status_code} - {response.text}")
                    response.raise_for_status()

        except requests.RequestException as e:
            logger.error(f"Request failed: {e}", e)
            raise e            
        except Exception as e:
            # Handle any exceptions or errors here
            logger.error(f"Unexpected Error: {e}", e)
            raise e
