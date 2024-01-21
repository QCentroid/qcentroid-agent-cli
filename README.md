# qcentroid-agent-cli

![deploy to pypi](https://github.com/QCentroid/qcentroid-agent-cli/actions/workflows/publish.yml/badge.svg)
[![Python](https://img.shields.io/pypi/pyversions/qcentroid-agent-cli.svg)](https://badge.fury.io/py/qcentroid-agent-cli)
[![PyPI](https://badge.fury.io/py/qcentroid-agent-cli.svg)](https://badge.fury.io/py/qcentroid-agent-cli)
 
Client library to interact with qcentroid agent API.



## Functions


Functions:
* obtain status, and context
* obtain input data 
* send output data
* set status
* send execution logs

## Install

```bash
pip install qcentroid-agent-cli
```


## Use

### Simple example

As easy as this:

```python
from qcentroid_agent_cli import QCentroidSolverClient
base_url="https://api.qcentroid.xyz"
api_key="1234-4567-8910"  # Get your solver API_KEY in the platform dashboard
solver_id="123"

def main():
    
    # Initialize the agent and get the solver details and a valid access token
    solver = QCentroidSolverClient(base_url, api_key, solver_id)

    # Request a queued job (the oldest one will be returned)
    job = solver.obtainJob()
    
    # Notify start of job execution
    job.start()
    
    # Retrieve the job input data
    input_data = job.obtainInputData()
    output_data = {} 

    #
    # TODO: Add your solver code here and generate output_data
    #

    # Send the solver output data and execution logs to the platform
    job.sendOutputData(output_data)
    job.sendExecutionLog(logs)
    
    
    
if __name__ == "__main__":
    main() 
```

### As external agent:

```python
import requests
from qcentroid_agent_cli import QCentroidSolverClient
base_url="https://api.qcentroid.xyz"
api_key="1234-4567-8910"  # Get your solver API_KEY in the platform dashboard
solver_id="123"

def main():
    exit = False
    print("QCentroid Agent example!")
    print("Starting...")
    
    # Initialize the agent by getting the solver details and a valid access token
    solver = QCentroidSolverClient(base_url, api_key, solver_id)

    print("Solver initialization succesful.")

    # Loop to request queued jobs until any exit condition you want to set
    while not exit:
        try:
            print("Checking for pending jobs...")
            # Request a queued job (the oldest one will be returned)
            job = solver.obtainJob()

            if job :
                print("New job received.")
                # There is a job to be processed!
                try:
                    print("Processing job...")
                    # Notify the platform we're starting to process this job
                    job.start()
                    # Retrieve the input data
                    input_data = job.obtainInputData()
                    output_data = {} 
                    
                    #
                    # TODO: add your solver code here and generate output_data
                    #

                    print("Job processed successfully.")
                    # Send the solver output data to the platform
                    job.sendOutputData(output_data)
                    # Send the solver execution logs to check them thorugh the platform dashboard
                    # TODO: job.sendExecutionLog(logs)
                    
                    job.end()              
                except Exception as e:
                    # Job execution has failed, notify the platform about the error
                    print("Error during job execution.")
                    job.error(e)

            else:        
                # No queued jobs. Wait for 1 minute and check again
                print("No pending jobs. Waiting for 1 minute...")
                time.sleep(60)
            
        except requests.RequestException as e:
            # Error in an API request
            # Whether parameters are incorrect (URL, api-key or solver_id), or there are connectivity issues
            print(f"QCentroid Agent: API request failed: {e}")
            exit=True
            
        except Exception as e:
            # Any other errors
            print(f"QCentroid Agent error: {e}")
            exit=True
            
    print("End.")


if __name__ == "__main__":
    main()

```

### As agent:

```python
from qcentroid_agent_cli import QCentroidAgentClient

base_url = "https://api.qcentroid.xyz"
# job-id from EXECUTION_ID env var
# token from QCENTROID_TOKEN env var

job = QCentroidAgentClient(base_url)
data = None
try:
  job.start()
  data = job.obtainData()
  #TODO job with data  
  job.sendData(data)
  job.end()
except BaseException as be:
  job.error(be)
#end

```
  
