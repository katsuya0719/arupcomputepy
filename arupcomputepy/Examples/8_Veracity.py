import arupcomputepy
import json

calcID = 2069141 # Veracity
jobNumber = '00000-00' # for testing only - please use a real job number

variables = {
    'Collection' : 'UK',
    'Type' : 'Concrete',
    'List Index Toggle' : True,
    'Index Selection' : 0,
    'Text Filter Toggle' : True,
    'Text Filter' : 'slag,20'
}

accessToken = arupcomputepy.AcquireNewAccessTokenDeviceFlow()

response = arupcomputepy.MakeCalculationRequest(calcID, jobNumber, accessToken, isBatch=False, variables=variables)

outputs = json.loads(response['output'])

retrievedItem = outputs['arupComputeResultItems']

print(retrievedItem)