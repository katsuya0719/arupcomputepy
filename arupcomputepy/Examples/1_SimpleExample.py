import arupcomputepy

library = 'designcheck'
calc_url = 'structural/yieldlines/rectangularfoursidessupported_15312'

variables = {
    'a': 3,
    'b': 5,
    'i_l': 0,
    'i_b': 0,
    'i_r': 0,
    'i_t': 0,
    'n': 1,
    'p_v': 0,
    'p_h': 0
}

response = arupcomputepy.Compute(library, calc_url, variables=variables)

print(response['result'])