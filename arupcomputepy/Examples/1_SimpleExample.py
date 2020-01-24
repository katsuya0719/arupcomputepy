import arupcomputepy
import json

calcID = 2761 # Civil > Calculate K value DC2 library version 0.0.0-beta475
jobNumber = '00000-00'

variables = {
    'ID': 'Test',
    'L': 1,
    'a': 1
}

# To call ArupCompute we must get an access token
# there are several ways (flows) for acquiring these
# the simples is the device code flow which will
# prompt the user to visit a microsoft website and
# paste a code as authentication
accessToken = arupcomputepy.AcquireNewAccessTokenDeviceFlow()

# Response is everything sent back by ArupCompute
response = arupcomputepy.MakeCalculationRequest(calcID, jobNumber, accessToken, False, variables=variables)

# The output from the calculation is JSON formatted
# We can convert it into python data structures using the
# built-in JSON library
output = json.loads(response['output'])

print(output['results_K']['value'])