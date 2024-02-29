from requests_toolbelt import MultipartEncoder
import requests
from requests.exceptions import HTTPError
import json
import os
import mimetypes
from io import StringIO
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
    # Convert dictionary to JSON string
    json_data:str = json.dumps(data)

    # Convert JSON string to a BufferedReader
    return StringIO(json_data)    

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
            response = requests.get(f"{self.base_url}/agent/job/{self.name}/data/input", headers=self.getHeaders())

            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                # Parse and use the response data as needed                
                data = processJsonData(response)            
                logger.debug(f"API Response:{data}")
                return data #return json 
            else:
                logger.error(f"Error: {response.status_code} - {response.text}")
                response.raise_for_status()

        except HTTPError as e:
            logger.exception(f"Request failed: ", str(e))
            raise e            
        except Exception as e:
            # Handle any exceptions or errors here
            logger.exception(f"Unexpected Error: ", str(e))            
            raise e

    #POST [core]/agent/job/{job_name}/data/output
    def sendOutputData(self, data:dict) -> bool:
        
        file = data2file(data)     
        
        headers = self.getHeaders()

        m = MultipartEncoder(
            fields={'file': ('output.json', file, 'application/json')}
        )   
        headers["Content-Type"] = m.content_type
        
        
        try:
            response = requests.post(f"{self.base_url}/agent/job/{self.name}/data/output", headers=headers, data=m)
            
            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                # Parse and use the response data as needed
                data = processJsonData(response)
                logger.debug(f"API Response:{data}")
                return True
            else:
                logger.error(f"Error: {response.status_code} - {response.text}")
                response.raise_for_status()

        except HTTPError as e:
            logger.exception(f"Request failed: ", str(e))
            raise e              
        except Exception as e:
            # Handle any exceptions or errors here
            logger.exception(f"Unexpected Error: ", str(e))
            raise e
        

    #POST /agent/job/{job_name}/data/output/additional
    def sendAdditionalOutputFile(self, filename:str) -> bool:

        try:
            with open(filename, "rb") as file:
                headers=self.getHeaders()
                m = MultipartEncoder(
                    fields={'file': (file.name, file)}
                )   
                headers["Content-Type"] = m.content_type
                response = requests.post(f"{self.base_url}/agent/job/{self.name}/data/output/additional", headers=headers, data=m)
                if response.status_code == 200:
                    # Parse and use the response data as needed
                    data = processJsonData(response)
                    logger.debug(f"API Response:{data}")
                    return True
                else:
                    logger.error(f"Error: {response.status_code} - {response.text}")
                    response.raise_for_status()

        except HTTPError as e:
            logger.exception(f"Request failed: ", str(e))
            raise e      
        except OSError as e:      
            logger.exception(f"Filenotfound:{filename}", str(e))
        except Exception as e:
            # Handle any exceptions or errors here
            logger.exception(f"Unexpected Error: ", str(e))
            raise e

    #GET [core]/agent/job/{job}/execution-log
    def sendExecutionLog(self, filename:str) -> bool:
        try:
           
            with open(filename, "rb") as file:
                headers=self.getHeaders()
                m = MultipartEncoder(
                    fields={'file': ('output.json', file, 'application/json')}
                )   
                headers["Content-Type"] = m.content_type
                response = requests.post(f"{self.base_url}/agent/job/{self.name}/execution-log", headers=headers, data=m)                
                if response.status_code == 200:
                    # Parse and use the response data as needed
                    data = processJsonData(response)
                    logger.debug(f"API Response:{data}")
                    return True
                else:
                    logger.error(f"Error: {response.status_code} - {response.text}")
                    response.raise_for_status()
        except HTTPError as e:
            logger.exception(f"Request failed: ", str(e))
            raise e             
        except OSError as e:
            logger.exception(f"FileError: ", str(e))
            raise e        
        except Exception as e:
            # Handle any other unexpected exceptions here
            logger.exception(f"Unexpected Error: ", str(e))
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
        
        except HTTPError as e:
            logger.exception(f"Error: e", str(e))
            raise e
        except Exception as e:
            # Handle any other unexpected exceptions here
            logger.exception(f"Unexpected Error: e", str(e))
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
            logger.exception(f"FileNotError:", str(e))
            raise e
        except HTTPError as e:
            logger.exception(f"Error: ",str(e))
            raise e
        except Exception as e:
            # Handle any other unexpected exceptions here
            logger.exception(f"Unexpected Error: ", str(e))
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

            
            if response.status_code == 200:
                # Parse and use the response data as needed
                data = processJsonData(response)
                logger.info(f"API Response:{data}")
                return QCentroidAgentClient(self.base_url, data["token"], data["name"]) #return  QCentroidAgentClient
                
                # No jobs
            elif response.status_code == 204:                
                return None
            else:
                logger.error(f"Error: {response.status_code} - {response.text}")
                response.raise_for_status()

        except HTTPError as e:
            logger.exception(f"Request failed: ", str(e))
            raise e            
        except Exception as e:
            # Handle any exceptions or errors here
            logger.exception(f"Unexpected Error: ", str(e))
            raise e
