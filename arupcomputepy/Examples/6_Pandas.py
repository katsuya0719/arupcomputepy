import arupcomputepy
import json

calcID = 2026567 # SlabOverallDepth v63.0.1
jobNumber = '00000-00' # for testing only - please use a real job number

l_input = [5, 5.5, 6, 6.5, 7, 7.5, 8, 8.5, 9, 9.5, 10]
slab_type_input = ['OneWaySolidSlab_SingleSpan'] * 11
q_k_input = [3.1] * 11
g_ksdl_input = [1.2] * 11

# Note that we use lists of input data for a batch calculation
variables = {
    'ID' : list(range(1,12)),
    'slab_type' : slab_type_input,
    'q_k' : q_k_input,
    'g_ksdl' : g_ksdl_input,
    'l' : l_input
}

accessToken = arupcomputepy.AcquireNewAccessTokenDeviceFlow()

# Note that we need to set the variable isBatch = True
response = arupcomputepy.MakeCalculationRequest(calcID, jobNumber, accessToken, isBatch=True, variables=variables)

outputs = json.loads(response['output'])

import pandas as pd

# Create DataFrame
df = pd.DataFrame(columns=['Slab Type', 'q_k (kPa)', 'g_ksdl (kPa)', 'Span (m)', 'Depth (mm)'])

for i in range(len(outputs)):
    df.loc[i] = [slab_type_input[i], q_k_input[i], g_ksdl_input[i], l_input[i], outputs[i]['arupComputeResultItems'][0]['value']]

print(df)