import requests
import json
import msal
import appdirs
import os
import atexit
import logging

def MakeCalculationRequest(calcID, jobNumber, accessToken, isBatch, variables=None, client='arupcomputepy', useArupProxy=False, timeout=None, resultType="mini"):
    '''
    Sends calculation(s) to the ArupCompute server for execution and returns the result.

    First time running will require the creation of an Azure access token. This will be guided via the console. Alternatively execute the 'AcquireAccessToken' function.

    Keyword arguments:
        calcID - calculation identifier, find using the ArupCompute web interface NOTE this is pegged to a specific library version and will NOT automatically be updated to take benefit from bugfixes
        jobNumber - jobNumber this calculation is associated with
        isBatch - is this a batch calculation (multiple calculations in one request)?
        variables -- Dictionary of variables to feed key = variable name, value = value to run (names and formatting as per ArupCompute URL). All required data types can be handled for example:
            variables = {}
            variables['alpha'] = 12.7
            variables['underground'] = False
            variables['mode'] = 'Special'
            variables['layers'] = [65,90,150]
        useArupProxy - try and use False initially, otherwise True may be required
        timeout - how long to wait for a server response before failing
        client - defaults to 'arupcomputepy' but if developing your own application utilising this library please override this
        clientId - required as part of the client secret flow, obtained from Azure App Registration
        clientSecret - the client secret associated with your app registration
        resultType - either "full" - everything that the library provides, "simple" - limited to ArupComputeResult (results, reports, messages), or "mini" - just results. Defaults to "mini".

    Returns:
        server response as JSON
    '''

    checkResultType = ['full','mini','simple']
    if (resultType not in checkResultType):
        raise Exception(f"Entered result type '{resultType}', but only 'full', 'simple', or 'mini' keyword arguments are allowed")

    endpoint = f'calcrecords?calcId={calcID}&jobNumber={jobNumber}&client={client}&isBatch={isBatch}&resultType={resultType}'
    
    return MakeGenericRequest(endpoint, accessToken, body=variables, useArupProxy=useArupProxy, timeout=timeout)

def MakeGenericRequest(endpoint, accessToken, body=None, timeout=None, useArupProxy=False):
    '''
    Sends a generic API request to ArupCompute. For API documentation look here https://arupcompute-dev.azurewebsites.net/api/docs/index.html

    Keyword arguments:
        endpoint - everything after https://compute.arup.digital/api, for example if you want to hit https://compute.arup.digital/api/CalcRecords just pass in 'CalcRecords'
        body - if you are hitting a POST endpoint put the payload here in JSON format
        accessToken - ArupCompute access token, use helper methods in arupcomputepy to obtain this (e.g. AcquireNewAccessTokenDeviceFlow, AcquireNewAccessTokenClientSecretFlow)
        timeout - how long to wait for a server response before failing
        useArupProxy - whether to use the Arup proxy servers or not (may be required where porous networking is not enabled)
    '''
    
    headers = {'Authorization': 'Bearer %s' % accessToken}

    # root = r'https://compute.arup.digital/api'
    root = r'https://arupcompute-dev.azurewebsites.net/api' # temporary for testing purposes

    url = root + '/' + endpoint
    
    if useArupProxy:

        proxyDict = {
            "http": "http://proxy.ha.arup.com:80",
            "https": "https://proxy.ha.arup.com:80"
        }
        
        if(body):
            r = requests.post(url, json=body, headers=headers, timeout=timeout, proxies=proxyDict)
        else:
            r = requests.get(url, headers=headers, timeout=timeout, proxies=proxyDict)

    else:
        if(body):
            r = requests.post(url, json=body, headers=headers, timeout=timeout)
        else:
            r = requests.get(url, headers=headers, timeout=timeout)

    r.raise_for_status() # check for failed responses e.g. 400

    if '<title>Sign in to your account</title>'.encode('utf-8') in r.content:
        raise SystemError('Connection has been unsuccessful, check authentication and / or proxy requirements. If unsuccessful raise an issue at https://gitlab.arup.com/arupcompute/arupcomputepy/issues')

    return json.loads(r.content)


def AcquireNewAccessTokenDeviceFlow(refreshToken=None):

    tenant = '4ae48b41-0137-4599-8661-fc641fe77bea'
    clientId = '765d8aec-a87c-4d7d-be95-b3456ef8b732'
    authority_url = 'https://login.microsoftonline.com/' + tenant
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

def AcquireNewAccessTokenClientSecretFlow(clientId, clientSecret):

    # https://github.com/AzureAD/microsoft-authentication-library-for-python/blob/dev/sample/confidential_client_secret_sample.py
    
    tenant = '4ae48b41-0137-4599-8661-fc641fe77bea'
    authority_url = 'https://login.microsoftonline.com/' + tenant
    scopes = ['api://df8247c5-9e83-4409-9946-6daf9722271a/.default']

    app = msal.ConfidentialClientApplication(clientId, authority=authority_url, client_credential=clientSecret)

    result = None

    result = app.acquire_token_silent(scopes, account=None)

    if not result:
        result = app.acquire_token_for_client(scopes=scopes)
    
    if "access_token" in result:
        return result['access_token']
    else:
        print(result.get("error"))
        print(result.get("error_description"))
        print(result.get("correlation_id"))  # You may need this when reporting a bug

def test():
    print('arupcomputepy has installed correctly')