import arupcomputepy
import json

# See 1_SimpleExample.py for additional comments

calcID = 2761
jobNumber = '00000-00'

# Note here that we use lists of input data to enable batch execution
variables = {
    'ID': ['Test1','Test2','Test3'],
    'a': [1,2,3],
    'L': [1,2,3]
}

accessToken = arupcomputepy.AcquireNewAccessTokenDeviceFlow()

responses = arupcomputepy.MakeCalculationRequest(calcID, jobNumber, accessToken, variables=variables)

for response in responses:
    output = json.loads(response['output'])
    print(output['results_K']['value'])