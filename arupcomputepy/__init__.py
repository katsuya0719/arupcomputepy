import requests
import json
import msal
import appdirs
import os
import atexit

def ComputeURL(url, variables=None, useArupProxy=False, timeout=10, client='arupcomputepy'):
    if variables is None: # None may be possible for a calculation that takes no inputs e.g. random number generator
        variables = {}

    root = r'https://compute.arup.digital/api'
    url = root + '/' + url + '?client=' + client # Tag API calls stating that they came from the python library, can be overridden if we want to collect different data

    accessToken = AcquireNewAccessToken()
    return MakeRequest(url, variables, timeout, accessToken, useArupProxy=useArupProxy)

def Compute(library, calculation, variables=None, useArupProxy=False, timeout=10, client='arupcomputepy'):
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
        server response as JSON
    '''
    url = '/'.join([library,calculation])
    return ComputeURL(url, variables=variables, useArupProxy=useArupProxy, timeout=timeout, client=client)

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


def AcquireNewAccessToken(refreshToken=None):

    tenant = '4ae48b41-0137-4599-8661-fc641fe77bea'
    clientId = '765d8aec-a87c-4d7d-be95-b3456ef8b732'
    authority_url = 'https://login.microsoftonline.com/' + tenant + '/v2.0'
    scopes = ["api://df8247c5-9e83-4409-9946-6daf9722271a/access_as_user"]

    # Cache implementation: https://msal-python.readthedocs.io/en/latest/index.html?highlight=PublicClientApplication#tokencache
    userDataDir = appdirs.user_data_dir('Compute','Arup')
    token_cache = os.path.join(userDataDir,'TokenCachePy.msalcache.bin')
    
    if not os.path.exists(userDataDir):
        os.makedirs(userDataDir)

    result = None
    cache = msal.SerializableTokenCache()
    if os.path.exists(token_cache):
        cache.deserialize(open(token_cache, "r").read())

    atexit.register(lambda:
        open(token_cache, "w").write(cache.serialize())
        # Hint: The following optional line persists only when state changed
        if cache.has_state_changed else None
        )

    app = msal.PublicClientApplication(clientId, authority=authority_url, token_cache=cache)
    accounts = app.get_accounts()
    if accounts:
        # If so, you could then somehow display these accounts and let end user choose
        # Assuming the end user chose this one
        chosen = accounts[0]
        print("Using default account: " + chosen["username"])
        # Now let's try to find a token in cache for this account
        result = app.acquire_token_silent(scopes, account=chosen)

    if not result:
        # So no suitable token exists in cache. Let's get a new one from AAD.
        flow = app.initiate_device_flow(scopes=scopes)
        print(flow["message"])
        # Ideally you should wait here, in order to save some unnecessary polling
        # input("Press Enter after you successfully login from another device...")
        result = app.acquire_token_by_device_flow(flow)  # By default it will block

    if "access_token" in result:
        return result['access_token']
    else:
        print(result.get("error"))
        print(result.get("error_description"))
        print(result.get("correlation_id"))  # You may need this when reporting a bug

def test():
    print('arupcomputepy has installed correctly')