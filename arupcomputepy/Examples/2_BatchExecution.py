import arupcomputepy
import json

# See 1_SimpleExample.py for additional comments

calcID = 2118 # Sample Library v2.0.8 Basic Calc
jobNumber = '00000-00' # for testing only - please use a real job number

# Note that we use lists of input data for a batch calculation
variables = {
    'a': [1,20,300],
    'b': [2,40,600]
}

accessToken = arupcomputepy.AcquireNewAccessTokenDeviceFlow()

# Note that we need to set the variable isBatch = True
response = arupcomputepy.MakeCalculationRequest(calcID, jobNumber, accessToken, isBatch=True, variables=variables)

outputs = json.loads(response['output'])

for output in outputs:
    print(output)