import arupcomputepy
import time
import matplotlib.pyplot as plt
import random

def MultiCall(number):

    print(f'Starting run ({number})')
    
    jobnumber = "00000"
    calcId = 166683 # DesignCheck2 v7.4.0 Peak Velocity Pressure
    
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
        variables['E'].append(random.uniform(290.0,300.0))
        variables['N'].append(random.uniform(45.0,55.0))
        variables['A'].append(random.uniform(100.0,125.0))
        variables['z'].append(random.uniform(8.0,10.0))
        variables['p'].append(0.02)
        variables['c_dir'].append(random.uniform(0.73,1.00))
        variables['c_season'].append(1.0)
        variables['c_o'].append(1.0)
        variables['h_ave'].append(5.0)
        variables['x'].append(2.0)
        variables['X_c'].append(random.uniform(50.0,80.0))
        variables['X_T'].append(random.uniform(2.0,5.0))

    start_time = time.time()

    token = arupcomputepy.AcquireNewAccessTokenDeviceFlow()
    responses = arupcomputepy.MakeCalculationRequest(calcId, jobnumber, token, isBatch=True, variables=variables, resultType="mini") # did batch execution so we get a list of responses instead of just one

    calcTime = time.time() - start_time
    calctimePer = calcTime / number

    print(f'Calculation run of ({number}) --- {calctimePer} seconds per --- ')

    return (calcTime, calctimePer)

# Main

testX = [1,2,4,8,16,32,64,128,256,512,1024,2048,4096,8192]
total = []
percalc = []
for x in testX:
    calcTime, calctimePer = MultiCall(x)
    total.append(calcTime)
    percalc.append(calctimePer)


fig = plt.figure()
ax = plt.axes()
ax.plot(testX, total)
ax.plot(testX, percalc)
plt.show()