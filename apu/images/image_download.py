#!python
# https://pan.dev/prisma-cloud/api/cspm/download-vulnerability-file-v-3/

import json

import requests

from apu.utils import login  # importing this should trigger the login procedure

url = f"{login.settings["url"]}/uve/api/v3/vulnerabilities/download"

payload = json.dumps(
    {
        "downloadRequests": [
            {
                "cveId": "CVE-2021-44228",
                "riskFactors": "Urgent, Patchable, Exploitable",
                "assetType": "package,serverlessFunction,iac,deployedImage,vmImage,registryImage,host",
            }
        ]
    }
)

response = requests.request("POST", url, headers=login.headers, data=payload)
response.raise_for_status()
print(response.text)
