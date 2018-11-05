from requests import Request, Session
import json
import asyncio
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

    req = Request('GET', '/'.join([root,library,calculation]), params=variables).prepare()
    return req.url

def ExecuteCalculationsSync(requests, useArupProxy=False, timeout=10):
    proxyDict = {
        "http": "http://proxy.ha.arup.com:80",
        "https": "https://proxy.ha.arup.com:80"
    }

    session = Session()

    contents = []
    for request in requests:
        if useArupProxy:
            r = session.get(request, proxies=proxyDict, timeout=timeout)
        else:
            r = session.get(request, timeout=timeout)

        contents.append(r.json())

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
            future = session.get(request, proxies=proxyDict, timeout=timeout)
        else:
            future = session.get(request, timeout=timeout)
        futures.append(future)

    contents = []
    for future in futures:
        response = future.result()
        contents.append(response.content)

    return contents