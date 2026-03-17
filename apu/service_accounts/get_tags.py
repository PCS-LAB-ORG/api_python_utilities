#!python



url = "https://api.prismacloud.io/api/v34.00/tags"

from pcpi import session_loader
session_managers = session_loader.load_config(file_path="/Users/jumiles/.prismacloud/lab_credentials.json") #(identifier_name=PRISMA_ACCESS_KEY, secret_name=PRISMA_SECRET_KEY, api_url_name=DOMAIN) # returns single session manager
session_man = session_managers[0]
cspm_session = session_man.create_cspm_session()

payload = {}
headers = {
  'Accept': 'application/json'
}
res = cspm_session.request("GET", "/api/v34.00/tags", payload)
print(res)
print(res.text)