import arupcomputepy
import json
import numpy as np

calcID = 2039369 # Two-pile pile cap check (UK NA) v63.0.2
jobNumber = '00000-00' # for testing only - please use a real job number

accessToken = arupcomputepy.AcquireNewAccessTokenDeviceFlow()

# Inital force range guesses
N_min = 100
N_max = 2000

batch_size = 20
tolerance = 0.005

while True:
    
    # Note that we use lists of input data for a batch calculation
    variables = {
        'N_Ed_ULS' : list(np.linspace(N_min, N_max, batch_size)),
        'ID' : [x for x in range(1,batch_size+1)],
        'N_layers_tens' : [2] * batch_size,
        'S_vert_tens' : [50] * batch_size,
        'Dia_Tens' : [32] * batch_size,
        'n_bars' : [8] * batch_size,
        's_piles' : [1800] * batch_size,
        'w_col' : [700] * batch_size,
        'd_col' : [700] * batch_size,
        'h_cap' : [1400] * batch_size,
        'd_cap' : [1000] * batch_size,
        'w_cap' : [2700] * batch_size,
        'gamma_G' : [1.35] * batch_size,
        'Dia_pile' : [600] * batch_size,
        'f_ck' : [32] * batch_size,
        'c_base' : [75] * batch_size,
        'c_sides' : [75] * batch_size,
        'gamma_C' : [1.5] * batch_size,
        'f_yk' : [500] * batch_size,
        'gamma_S' : [1.15] * batch_size,
        'l_prov' : [200] * batch_size
    }

    # Note that we need to set the variable isBatch = True
    response = arupcomputepy.MakeCalculationRequest(calcID, jobNumber, accessToken, isBatch=True, variables=variables)

    outputs = json.loads(response['output'])
    
    # If utilisation of 1.0 is not between N_min and N_max, adjust range appropriately
    if outputs[0]['arupComputeResultItems'][len(outputs[0]['arupComputeResultItems'])-1]['value'] > 1.0:
        N_min = N_min / 2
        continue        
    if outputs[len(outputs)-1]['arupComputeResultItems'][len(outputs[len(outputs)-1]['arupComputeResultItems'])-1]['value'] < 1.0:
        N_max = N_max * 2
        continue
    
    # Loop over batch results
    for i in range(len(outputs)):
        
        utilisation = outputs[i]['arupComputeResultItems'][len(outputs[i]['arupComputeResultItems'])-1]['value']
        N_current = variables['N_Ed_ULS'][i]
        
        # Check if found capacity within tolerance
        if abs(1-utilisation) < tolerance:
            print(f"The capacity of the pile cap is: {round(N_current,1)} kN")
            break;
            
        # Update N_min
        if utilisation < 1:
            N_min = N_current
            
        # Update N_max
        if utilisation > 1 and N_current < N_max:
            N_max = N_current
    else:
        continue
        
    break
    