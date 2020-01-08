import arupcomputepy
import json

calcID = 2761 # Civil > Calculate K value DC2 library version 0.0.0-beta475
jobNumber = '00000-00'

variables = {
    'ID': ['Test1','Test2','Test3'],
    'a': [1,2,3],
    'L': [1,2,3]
}

# Response is everything sent back by ArupCompute
responses = arupcomputepy.Compute(calcID, jobNumber, variables=variables)

for response in responses:
    output = json.loads(response['output'])
    print(output['results_K']['value'])