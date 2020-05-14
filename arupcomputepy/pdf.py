import requests
import json
import os
from pathlib import Path

def Create(html, name, path, replace=False):
    '''
    Utilises the ArupCompute PDF creation service to render HTML to an Arup-branded calculation
    sheet and then saves it to a local file.

    Note this is a relatively expensive operation that runs on a small service in the cloud that can be quickly
    overwhelmend. Please do not overload this service as it is the same one that is used by the web interface.

    Keyword arguments:
        html - html content (e.g. from DesignCheck calculation)
        name - author name to appear on headers of calculation sheet
        path - filepath to save the created PDF to
        replace - boolean - set to true to overwrite existing files, otherwise an error will be thrown
    '''

    if(replace == False):
        if(os.path.exists(path)):
            raise Exception('File already exists at location: ' + path)

    # Check path before creating request
    # Note requires python >= 3.5
    Path(os.path.dirname(path)).mkdir(parents=True, exist_ok=True)
    
    pdfserviceurl = 'https://arupcompute-web-pdf.azurewebsites.net/'

    argumentdict = {}
    argumentdict['name'] = name
    argumentdict['arupComputeReport_HTML'] = html

    response = requests.post(pdfserviceurl, json=argumentdict)

    response.raise_for_status()

    with open(path, 'wb') as f:
        f.write(response.content)