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
from qcentroid-agent-cli import QCentroidSolverClient
base_url="https://api.qcentroid.xyz"
api_key="1234-4567-8910"
solver_id="123"

def main():
    
    print("Hello QCentroid Agent!")
    solver = QCentroidSolverClient(base_url, api_key, solver_id)

    while True: # put some escape function
        agent = solver.obtainJob()

        if agent :
            execute_job(agent)

        # Wait for 1 minute before the next iteration
        time.sleep(60)
   

if __name__ == "__main__":
    main()

```

As agent:

```python
from qcentroid-agent-cli import QCentroidAgentClient()

base_url = "https://api.qcentroid.xyz"
# job-id from EXECUTION_ID env var
# token from QCENTROID_TOKEN env var

agent = QCentroidAgentClient(base_url)
data = None
try:
  agent.start()
  data = agent.obtainData()
  #TODO job with data  
  agent.sendData(data)
  agent.end()
catch BaseException be:
  agent.error(be)
#end

```
  
