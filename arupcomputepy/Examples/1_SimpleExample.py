import arupcomputepy
import json

calcID = 304390 # Sample Library v2.1.62 Basic Calc
jobNumber = '00000-00' # for testing only - please use a real job number

variables = {
    'a': 1,
    'b': 2
}

# To call ArupCompute we must get an access token
# there are several ways (flows) for acquiring these
# the simples is the device code flow which will
# prompt the user to visit a microsoft website and
# paste a code as authentication
accessToken = arupcomputepy.AcquireNewAccessTokenDeviceFlow()

# Response is everything sent back by ArupCompute
response = arupcomputepy.MakeCalculationRequest(calcID, jobNumber, accessToken, isBatch=False, variables=variables)

# The output from the calculation is JSON formatted
# We can convert it into python data structures using the
# built-in JSON library
# The complexity of the return data structure is calculation-dependent
output = json.loads(response['output'])

print(output)