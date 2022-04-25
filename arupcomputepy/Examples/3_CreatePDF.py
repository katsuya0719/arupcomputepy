import arupcomputepy
import arupcomputepy.pdf
import json
import tempfile
import os

calcID = 5049731 # DesignCheck2 v131.1.0 Examples.SimpleCalculation
jobNumber = '00000-00' # for testing only - please use a real job number

variables = {
    'ID': 'Test',
    'A': 1,
    'B': 2
}

accessToken = arupcomputepy.AcquireNewAccessTokenDeviceFlow()

 # Note: must use 'simple' or 'full' result type to get HTML from library (the default 'mini' just returns numbers to keep response size down)
response = arupcomputepy.MakeCalculationRequest(calcID, jobNumber, accessToken, isBatch=False, variables=variables, resultType='simple')

output = json.loads(response['output'])
html = output['arupComputeReport_HTML']

path = os.path.join(tempfile.gettempdir(),'arupcomputepy','arupcompute.pdf') # tempoary file location for demonstration purposes
print(path)

arupcomputepy.pdf.Create(html, "A.Nonymous", path)