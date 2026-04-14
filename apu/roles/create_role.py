from datetime import datetime
from prismacloud.api import pc_api

now = datetime.now()
role_list = []

for user_role_name in role_list:

    user_role_name = ""

    payload = {
        # "accountGroupIds": [
        #   "string"
        # ],
        # "additionalAttributes": {
        #   "hasDefenderPermissions": True,
        #   "onlyAllowCIAccess": True,
        #   "onlyAllowComputeAccess": True
        # },
        # "codeRepositoryIds": repo_array,
        "description": f"Today is {now}",
        "name": user_role_name,
        # "resourceListIds": [
        #   "string"
        # ],
        # "restrictDismissalAccess": True,
        "roleType": "string",
    }

    pc_api.user_role_create(payload)
