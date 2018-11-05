import ArupCompute
import time

library = 'designcheck'
calculation = 'structural/concrete/ns_3473/constructionjointcapacity'

variables = {
    'tau_cd': 0.0,
    'A_c': 700000,
    'f_sd': 400,
    'A_s': 1932,
    'alpha': 90,
    'mu': 1.5,
    'sigma_c': 0,
    'f_cd': 26.5
}

start = time.time()

number = 100
print('Number of calculations: ' + str(number))

# Prepare requests
requests = []
for x in range (0, number):
    request = ArupCompute.PrepareInputs(library, calculation, variables)
    requests.append(request)

print('Sync')
responses = ArupCompute.ExecuteCalculationsSync(requests, useArupProxy=True)

#print(responses)

syncend = time.time()
duration = syncend - start
print('Total time: ' + str(duration))
print('Avg. time: ' + str(duration * 1000 / number) + 'ms')

print('ASync')
responses = ArupCompute.ExecuteCalculationsAsync(requests, useArupProxy=True)

#print(responses)

asyncend = time.time()
duration = asyncend - syncend
print('Total time: ' + str(duration))
print('Avg. time: ' + str(duration * 1000 / number) + 'ms')