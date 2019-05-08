import arupcomputepy

library = 'designcheck'
calc_url = 'structural/yieldlines/rectangularfoursidessupported_15312'

# Pass in lists for the variables to enable batch execution
variables = {
    'a': [3,4,5],
    'b': [5,6,7],
    'i_l': [0,0,0],
    'i_b': [0,0,0],
    'i_r': [0,0,0],
    'i_t': [0,0,0],
    'n': [1,1,1],
    'p_v': [0,0,0],
    'p_h': [0,0,0]
}

responses = arupcomputepy.Compute(library, calc_url, variables=variables) # did batch exceution so we get a list of responses instead of just one

for response in responses:
    print(response['result'])