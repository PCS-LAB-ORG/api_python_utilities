#!python
# https://pan.dev/prisma-cloud/api/cspm/download-vulnerability-file-v-3/

import requests
import json


from apu.utils import login, http_logging # importing this should trigger the login procedure

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