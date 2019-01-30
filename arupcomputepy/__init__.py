import requests
import json
import adal
import appdirs
import os

def Compute(library, calculation, variables=None, useArupProxy=False, timeout=10):
    '''
    Sends calculation(s) to the ArupCompute server for execution and returns the result.

    First time running will require the creation of an Azure access token. This will be guided via the console. Alternatively execute the 'AcquireAccessToken' function.

    Keyword arguments:
        library -- ArupCompute library to use (as string) e.g. 'designcheck'
        calculation -- ArupCompute calculation to run (as string, formatted as per ArupCompute website URL) e.g. 'structural/concrete/ns_3473/constructionjointcapacity'
        variables -- Dictionary of variables to feed key = variable name, value = value to run (names and formatting as per ArupCompute URL). All required data types can be handled for example:
            variables = {}
            variables['alpha'] = 12.7
            variables['underground'] = False
            variables['mode'] = 'Special'
            variables['layers'] = [65,90,150]
        useArupProxy - try and use False initially, otherwise True may be required
        timeout - how long to wait for a server response before failing

    Returns:
        request object ready for execution (use arupcomputepy.ExecuteCalculations)
    '''
    
    if variables is None: # None may be possible for a calculation that takes no inputs e.g. random number generator
        variables = {}
    
    if 'client' not in variables:
        variables['client'] = 'arupcomputepy' # Tag API calls stating that they came from the python library, can be overridden if required (e.g by designcheckpy)
    
    root = r'https://compute.arup.digital/api'
    url = '/'.join([root,library,calculation])

    accessToken = AcquireToken()
    
    try:
        return MakeRequest(url, variables, timeout, accessToken, useArupProxy=useArupProxy)
    except:
        pass # most likely a token error, try again with a new one before falling over

    accessToken = AcquireNewAccessToken()
    return MakeRequest(url, variables, timeout, accessToken, useArupProxy=useArupProxy)

def MakeRequest(url, variables, timeout, accessToken, useArupProxy=False):
    headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer %s' % accessToken}
    
    if useArupProxy:

        proxyDict = {
            "http": "http://proxy.ha.arup.com:80",
            "https": "https://proxy.ha.arup.com:80"
        }

        r = requests.post(url, json=variables, headers=headers, timeout=timeout, proxies=proxyDict)

    else:
        r = requests.post(url, json=variables, headers=headers, timeout=timeout)

    r.raise_for_status() # check for failed responses e.g. 400

    if '<title>Sign in to your account</title>'.encode('utf-8') in r.content:
        raise SystemError('ArupCompute servers blocked to python access. Contact Matteo Cominetti to request that access be reopened.')
    
    return json.loads(r.content)

def AcquireToken():
    userDataDir = appdirs.user_data_dir('arupcomputepy','arupcompute')
    refreshTokenPath = os.path.join(userDataDir,'refreshToken.txt')

    if os.path.isfile(refreshTokenPath):
        with open(refreshTokenPath) as f:
            refreshToken = f.read().rstrip()
        return AcquireNewAccessToken(refreshToken=refreshToken)
    else:
        return AcquireNewAccessToken()

def AcquireNewAccessToken(refreshToken=None):

    authorityHostUrl = 'https://login.windows.net/'
    tenant = 'arup.onmicrosoft.com'
    resource = 'cd7cf9f0-b6a0-4cf0-a363-a023d9e2595d'
    clientId = '765d8aec-a87c-4d7d-be95-b3456ef8b732'
    authority_url = authorityHostUrl + '/' + tenant

    context = adal.AuthenticationContext(
    authority_url, validate_authority=tenant != 'adfs',
    )

    if refreshToken == None:
        code = context.acquire_user_code(resource, clientId)
        print(code['message']) # there is a risk that if the user cannot see this the program will hang indefinitely
        response = context.acquire_token_with_device_code(resource, code, clientId)
    else:
        response = context.acquire_token_with_refresh_token(refreshToken, clientId, resource)

    # Save the refresh token for next time
    refreshToken = response['refreshToken']
    userDataDir = appdirs.user_data_dir('arupcomputepy','arupcompute')
    refreshTokenPath = os.path.join(userDataDir,'refreshToken.txt')
    if not os.path.exists(userDataDir):
        os.makedirs(userDataDir)
    with open(refreshTokenPath, 'w') as f:
        f.write(refreshToken)

    return response['accessToken']

def test():
    print('arupcomputepy has installed correctly')