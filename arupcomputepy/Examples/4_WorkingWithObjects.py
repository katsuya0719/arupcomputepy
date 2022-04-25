import arupcomputepy
import json

def VariableDict(Symbol,Units,Description,HTMLLatex,Value):
    vd = {
        "Symbol": Symbol,
        "Units": Units,
        "Description": Description,
        "Latex": HTMLLatex,
        "Value": Value
    }
    return vd

calcID = 5049828 # DesignCheck2 v.131.1.0 Framework > Calculation with HTML - variables
jobNumber = '00000-00' # for testing only - please use a real job number

a = VariableDict('a','mm','I am a','a_{a}',3)
b = VariableDict('b','mm','I am b','b_{b}',4)
dcVariables = [a,b]

acVariables = {
    'calculatedVariable': 'c',
    'expression': 'a_{a} * Pow(b_{b},3)',
    'variables': dcVariables
}

print(acVariables)

accessToken = arupcomputepy.AcquireNewAccessTokenDeviceFlow()

response = arupcomputepy.MakeCalculationRequest(calcID, jobNumber, accessToken, isBatch=False, variables=acVariables, resultType='full')

output = json.loads(response['output'])

print(output)