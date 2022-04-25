import arupcomputepy
import json

# See 1_SimpleExample.py for additional comments

calcID = 2081643  # Sample Library v2.1.60 Examples.BasicUse > Basic Calc
jobNumber = '00000-00' # for testing only - please use a real job number

# Note that we use lists of input data for a batch calculation
variables = {
    'a': [1,20,300,4000,500,60],
    'b': [2,40,600,7000,800,90]
}

accessToken = arupcomputepy.AcquireNewAccessTokenDeviceFlow()

# Note that we need to set the variable isBatch = True
response = arupcomputepy.MakeCalculationRequest(calcID, jobNumber, accessToken, isBatch=True, variables=variables)

outputs = json.loads(response['output'])

for output in outputs:
    print(output)