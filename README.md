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

As external agent:

```python
from qcentroid_agent_cli import QCentroidSolverClient
base_url="https://api.qcentroid.xyz"
api_key="1234-4567-8910"
solver_id="123"

def main():
    
    print("Hello QCentroid Agent!")
    solver = QCentroidSolverClient(base_url, api_key, solver_id)
    exit = False
    while not exit: # put some escape function
      try:
        job = solver.obtainJob()

        if job :
          try:
            job.start()
            input_data = job.obtainInputData()
            output_data = {} 
            #TODO: add your code here to generate output_data
            job.sendOutputData(output_data)
            #TODO: job.sendExecutionLog(logs)
            job.end()              
          except Exception as e:
            # job execution has failed, notify the platform about the error
            job.error(e)
        else:        
          # Wait for 1 minute before the next iteration
          time.sleep(60)    
      except requests.RequestException as e:
        # parameters are incorrect, url, api-key or solver_id, or infrastructure
        print(f"Request failed: {e}")
        exit=True       

      
   

if __name__ == "__main__":
    main()

```

As agent:

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
  
