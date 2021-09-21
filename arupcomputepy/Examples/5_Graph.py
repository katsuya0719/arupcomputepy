import arupcomputepy
import json
import matplotlib.pyplot as plt

calcID = 2026567 # SlabOverallDepth v63.0.1
jobNumber = '00000-00' # for testing only - please use a real job number

# Note that we use lists of input data for a batch calculation
variables = {
    'ID' : [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
    'slab_type' : ['OneWaySolidSlab_SingleSpan', 'OneWaySolidSlab_SingleSpan', 'OneWaySolidSlab_SingleSpan', 'OneWaySolidSlab_SingleSpan', 'OneWaySolidSlab_SingleSpan', 'OneWaySolidSlab_SingleSpan', 'OneWaySolidSlab_SingleSpan', 'OneWaySolidSlab_SingleSpan', 'OneWaySolidSlab_SingleSpan', 'OneWaySolidSlab_SingleSpan', 'OneWaySolidSlab_SingleSpan'],
    'q_k' : [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    'g_ksdl' : [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    'l' : [5, 5.5, 6, 6.5, 7, 7.5, 8, 8.5, 9, 9.5, 10]
}

accessToken = arupcomputepy.AcquireNewAccessTokenDeviceFlow()

# Note that we need to set the variable isBatch = True
response = arupcomputepy.MakeCalculationRequest(calcID, jobNumber, accessToken, isBatch=True, variables=variables)

outputs = json.loads(response['output'])

# Create x- and y-series
x = json.loads(response['body'])['l']
y = [output['arupComputeResultItems'][0]['value'] for output in outputs]



ax = plt.axes()

ax.plot(x, y)
plt.xlabel('span (m)')
plt.ylabel('depth (mm)')

# Save figure
plt.savefig('arupcomputepy/Examples/ExampleOutput/GraphExample.png')