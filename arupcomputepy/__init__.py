from requests import Request, Session
import json
from requests_futures.sessions import FuturesSession
from concurrent.futures import ThreadPoolExecutor

def PrepareInputs(library, calculation, variables):
    '''
    Prepares a single calculation for execution via ArupCompute.

    Useful when running multiple checks as it allows asynchronous execution which is significantly faster than serial execution
    when communicating with a remote cloud computing service.

    Keyword arguments:
        library -- ArupCompute library to use (as string) e.g. 'designcheck'
        calculation -- ArupCompute calculation to run (as string, formatted as per ArupCompute website URL) e.g. 'structural/concrete/ns_3473/constructionjointcapacity'
        variables -- Dictionary of variables to feed key = variable name, value = value to run (names and formatting as per ArupCompute URL)

    Returns:
        Request URL
    '''
    
    root = r'https://arupcompute-dev.azurewebsites.net/api' #dev website does not have troublesome Microsoft authentication enabled - temporary solution only

    req = Request('POST', '/'.join([root,library,calculation]), json=variables).prepare()
    
    return req

def ExecuteCalculationsSync(requests, useArupProxy=False, timeout=10):
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

        contents.append(json.loads(r.content))

    return contents


def ExecuteCalculationsAsync(requests, useArupProxy=False, timeout=10, max_workers=None):

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
        contents.append(json.loads(future.content))

    return contents

def test():
    print('arupcomputepy has installed correctly')