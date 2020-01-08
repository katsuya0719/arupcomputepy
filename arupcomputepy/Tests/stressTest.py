import arupcomputepy
import time
import matplotlib.pyplot as plt

def MultiCall(number):

    print(f'Starting run ({number})')
    
    library = 'designcheck'
    calc_url = 'structural/yieldlines/rectangularfoursidessupported_15312'
    
    variables = {
    'a': [],
    'b': [],
    'i_l': [],
    'i_b': [],
    'i_r': [],
    'i_t': [],
    'n': [],
    'p_v': [],
    'p_h': []
    }

    for x in range (0, number):
        variables['a'].append(3),
        variables['b'].append(5),
        variables['i_l'].append(0),
        variables['i_b'].append(0),
        variables['i_r'].append(0),
        variables['i_t'].append(0),
        variables['n'].append(1),
        variables['p_v'].append(0),
        variables['p_h'].append(0),

    start_time = time.time()

    responses = arupcomputepy.Compute(library, calc_url, variables=variables, timeout=None) # did batch execution so we get a list of responses instead of just one

    calcTime = time.time() - start_time
    calctimePer = calcTime / number

    print(f'Calculation run of ({number}) --- {calctimePer} seconds per --- ')

    return calctimePer

# Main

testX = [1,10,100,500]
testY = []
for x in testX:
    try:
        testY.append(MultiCall(x))
    except:
        print(f'Calculation run {number} failed')
        continue

fig = plit.figure()
ax = plt.aces()
ax.plot(testX, testY)
plt.show()