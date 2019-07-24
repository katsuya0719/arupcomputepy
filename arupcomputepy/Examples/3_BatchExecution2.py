# -*- coding: utf-8 -*-
"""
Created on Fri Jul 19 14:36:45 2019

@author: Paul.Bailie
"""

import arupcomputepy as acp

acp.test()

library = 'designcheck'
calc_url = 'geotechnical/shallowfoundations/ec7/undrained_38b53'

# variables input as either single value or list of values per parameter
variables = {
        'V_g': [200,250],
        'V_q': [0,0],
        'H_g': [0,0],
        'H_q': [0,0],
        'Ml_g': [20, 20],
        'Ml_q': [0,0],
        'Mb_g': [20, 20],
        'Mb_q': [0,0],
        'B': [5,5],
        'L': [5,5],
        'q': [10,10],
        'alpha': [5,5],
        'c_u': [100,100],
        'gamma_g': [1.2,1.2],
        'gamma_q': [1.35,1.35],        
        'gamma_cu': [1.0,1.0],       
        'gamma_R': [1.0,1.0]
} 

results = []

responses = acp.Compute(library, calc_url, variables=variables) # type is 'dict' for single value or 'list' for multiple value input

if isinstance(responses, list):
    for response in responses:
        results.append(response['result'])
else:
    results.append(responses['result'])

print(results) # results output as list of one or more values

