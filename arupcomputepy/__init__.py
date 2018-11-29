from requests import Request, Session
import json
from requests_futures.sessions import FuturesSession
from concurrent.futures import ThreadPoolExecutor

def PrepareInputs(library, calculation, variables=None):
    '''
    Prepares a single calculation for execution via ArupCompute.

    Useful when running multiple checks as it allows asynchronous execution which is significantly faster than serial execution
    when communicating with a remote cloud computing service.

    Keyword arguments:
        library -- ArupCompute library to use (as string) e.g. 'designcheck'
        calculation -- ArupCompute calculation to run (as string, formatted as per ArupCompute website URL) e.g. 'structural/concrete/ns_3473/constructionjointcapacity'
        variables -- Dictionary of variables to feed key = variable name, value = value to run (names and formatting as per ArupCompute URL). All required data types can be handled for example:
            variables = {}
            variables['alpha'] = 12.7
            variables['underground'] = False
            variables['mode'] = 'Special'
            variables['layers'] = [65,90,150]

    Returns:
        request object ready for execution (use arupcomputepy.ExecuteCalculations)
    '''

    if variables is None: #None may be possible for a calculation that takes no inputs e.g. random number generator
        variables = {}
    
    variables['client'] = 'arupcomputepy' #Tag API calls stating that they came from the python library, only tracked on main branch
    
    root = r'https://arupcompute-dev.azurewebsites.net/api' #dev website does not have troublesome Microsoft authentication enabled - temporary solution only

    req = Request('POST', '/'.join([root,library,calculation]), json=variables).prepare()
    
    return req

def ExecuteCalculationsSync(requests, useArupProxy=False, timeout=10):
    '''
    Executes a list of previously prepared calculations via ArupCompute.
    Operates in a synchronous manner, but has less overhead than ExecuteCalculationsAsync.

    Keyword arguments:
        requests - list of request objects (prepare using PrepareInputs)
        useArupProxy - try and use False initially, otherwise True may be required
        timeout - how long to wait for a server response before failing

    Returns:
        JSON server response converted into python objects using the command json.loads()
    '''
    
    proxyDict = {
        "http": "http://proxy.ha.arup.com:80",
        "https": "https://proxy.ha.arup.com:80"
    }

    session = Session()

    contents = []
    for request in requests:
        if useArupProxy:
            r = session.send(request, proxies=proxyDict, timeout=timeout)
        else:
            r = session.send(request, timeout=timeout)

        r.raise_for_status() # check for failed responses e.g. 400

        if '<title>Sign in to your account</title>'.encode('utf-8') in r.content:
            raise SystemError('ArupCompute servers blocked to naive python access. Contact Matteo Cominetti to request that access be reopened.')
        
        contents.append(json.loads(r.content))

    return contents


def ExecuteCalculationsAsync(requests, useArupProxy=False, timeout=10, max_workers=None):
    '''
    Executes a list of previously prepared calculations via ArupCompute.
    Operates in an asynchronous manner, but has more overhead than ExecuteCalculationsSync.

    Keyword arguments:
        requests - list of request objects (prepare using PrepareInputs)
        useArupProxy - try and use False initially, otherwise True may be required
        timeout - how long to wait for a server response before failing
        max_workers - number of threads to use, defaults to 5 x no. of processors assuming IO bound

    Returns:
        JSON server response converted into python objects using the command json.loads()
    '''

    proxyDict = {
        "http": "http://proxy.ha.arup.com:80",
        "https": "https://proxy.ha.arup.com:80"
    }
    
    session = FuturesSession(executor=ThreadPoolExecutor(max_workers=max_workers))

    futures = []
    for request in requests:
        
        if useArupProxy:
            future = session.send(request, proxies=proxyDict, timeout=timeout)
        else:
            future = session.send(request, timeout=timeout)
        futures.append(future)

    contents = []
    for future in futures:
        future.raise_for_status() # check for failed responses e.g. 400

        if '<title>Sign in to your account</title>'.encode('utf-8') in future.content:
            raise SystemError('ArupCompute servers blocked to naive python access. Contact Matteo Cominetti to request that access be reopened.')

        contents.append(json.loads(future.content))

    return contents

def test():
    print('arupcomputepy has installed correctly')