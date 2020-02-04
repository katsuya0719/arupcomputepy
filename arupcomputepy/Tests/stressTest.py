import arupcomputepy
import time
import matplotlib.pyplot as plt
import logging

def MultiCall(number):

    print(f'Starting run ({number})')
    
    jobnumber = "00000"
    calcId = 3694
    
    variables = {
    'ID': [],
    'E': [],
    'N': [],
    'A': [],
    'z': [],
    'p': [],
    'c_dir': [],
    'c_season': [],
    'c_o': [],
    'h_ave': [],
    'x': [],
    'X_c': [],
    'X_T': []
    }

    for x in range (0, number):
        variables['ID'].append('Stress test')
        variables['E'].append(300)
        variables['N'].append(50)
        variables['A'].append(112)
        variables['z'].append(9.0)
        variables['p'].append(0.02)
        variables['c_dir'].append(0.73)
        variables['c_season'].append(1.0)
        variables['c_o'].append(1.0)
        variables['h_ave'].append(5.0)
        variables['x'].append(2.0)
        variables['X_c'].append(70.0)
        variables['X_T'].append(4.5)

    start_time = time.time()

    token = arupcomputepy.AcquireNewAccessTokenDeviceFlow()
    responses = arupcomputepy.MakeCalculationRequest(calcId, jobnumber, token, isBatch=True, variables=variables) # did batch execution so we get a list of responses instead of just one

    calcTime = time.time() - start_time
    calctimePer = calcTime / number

    print(f'Calculation run of ({number}) --- {calctimePer} seconds per --- ')

    return calctimePer

# Main

testX = [5,6]
testY = []
for x in testX:
    testY.append(MultiCall(x))

fig = plt.figure()
ax = plt.axes()
ax.plot(testX, testY)
plt.show()