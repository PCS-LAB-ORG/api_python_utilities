#!python
# https://pan.dev/prisma-cloud/api/cspm/download-vulnerability-file-v-3/

import requests
import json

from pathlib import Path
import sys, os
from prismacloud.api import pc_api

sys.path.append(os.path.abspath(f"../../../local/utility_scripts"))
from creds_lab import PRISMA_ACCESS_KEY, PRISMA_SECRET_KEY
settings = {
    "url": "https://api2.prismacloud.io",
    "identity": PRISMA_ACCESS_KEY,
    "secret": PRISMA_SECRET_KEY
}
pc_api.configure(settings=settings)


headers = {
  'Content-Type': 'application/json',
  'Accept': 'application/octet-stream',
  'x-redlock-auth': pc_api.token
}

url = f"{settings["url"]}/uve/api/v3/vulnerabilities/download"

payload = json.dumps({
  "downloadRequests": [
    {
      "cveId": "CVE-2021-44228",
      "riskFactors": "Urgent, Patchable, Exploitable",
      "assetType": "package,serverlessFunction,iac,deployedImage,vmImage,registryImage,host"
    }
  ]
})

response = requests.request("POST", url, headers=headers, data=payload)
response.raise_for_status()
print(response.text)