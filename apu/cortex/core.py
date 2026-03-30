from apu.cortex import jrequest

def get_alerts(payload=None):
    url = "alerts/get_alerts"

    payload = {
        "request_data": {
            # "filters": {}},
            # "alerts_limit": 1000 # default 1000
        }
    }

    response = jrequest.post(url, payload)
    return response

def issue_search(payload=None):
    url = "issue/search"

    payload = {
        "request_data": {
            "filters": [{"field": "issue_id", "operator": "in", "value": [0]}],
            "search_from": 0,
            "search_to": 2,
            "sort": {"field": "issue_id", "keyword": "asc"},
        }
    }
    response = jrequest.post(url, payload)
    return response

def get_datasets(payload=None):
    url = "xql/get_datasets"
    payload = { "request_data": {} }
    response = jrequest.post(url, payload)
    return response

def get_endpoints(payload=None):
    url = "endpoints/get_endpoints"
    payload = { "request_data": {} }
    response = jrequest.post(url, payload)
    return response

def get_incidents(payload=None):
    url = "alerts/get_incidents"
    payload = { "request_data": {} }
    response = jrequest.post(url, payload)
    return response

def unified_cli_releases_version():
    url = "unified-cli/releases/version"
    response = jrequest.get(url)
    return response

def case_search(payload=None):
    url = "case/search"
    payload = {
        "request_data": {
            "filters": [{"field": "severity", "operator": "in", "value": ["HIGH"]}],
            "search_from": 0,
            "search_to": 2,
            "sort": {"field": "case_id", "keyword": "asc"},
        }
    }
    response = jrequest.post(url, payload)
    return response

def xql_lookups_get_data(payload=None):
    url = "xql/lookups/get_data"
    dataset_name = "asdfsa" # for debugging 'a' is an existing table
    # if dataset_name and not len(sys.argv) > 1:
    #     raise Exception("Table name is required")
    # dataset_name = sys.argv[1]

    limit = 20
    # if len(sys.argv) > 2:
    #     limit = int(sys.argv[2])

    filters = []
    # if len(sys.argv) > 3:
    #     filters = json.loads(sys.argv[3])
    # [
        # {
        #     # "uid": "123",
        #     "user_email": "hiep@abc.com"
        # },
        # {
        #     "department": "dev",
        #     "zipcode": "58674"
        # }
    # ],

    payload = {
        "request": {
            "dataset_name": dataset_name,
            "filters": filters,
            "limit": limit
        }
    }

    response = jrequest.post(url, payload)
    return response

def incidents_extra_data(payload=None):
    url = "incidents/get_incident_extra_data"
    payload = {
        "request_data": {
            "incident_id": "",
            # "alerts_limit": 1000 # default 1000
        }
    }
    response = jrequest.post(url, payload)
    return response

def asset_groups(payload=None):
    url = "asset-groups"
    payload = {
        "request_data": {
            #     "AND": [
            #         {
            #             "SEARCH_FIELD": "XDM.ASSET_GROUP.TYPE",
            #             "SEARCH_TYPE": "EQ",
            #             "SEARCH_VALUE": "Dynamic",
            #         }
            #     ]
            # },
            # "sort": [{"FIELD": "XDM.ASSET_GROUP.LAST_UPDATE_TIME", "ORDER": "DESC"}],
            # "search_from": 0,
            # "search_to": 1000,
        }
    }
    response = jrequest.post(url, payload)
    return response

def get_issues(payload=None):
    url = "issue/search"

    payload = {
        "request_data": {
            "filters": [{"field": "issue_id", "operator": "in", "value": [0]}],
            "search_from": 0,
            "search_to": 2,
            "sort": {"field": "issue_id", "keyword": "asc"},
        }
    }
    response = jrequest.post(url, payload)
    return response

def get_roles(payload=None):
    url = "rbac/get_roles"

    payload = {}
    response = jrequest.post(url, payload)
    return response

def syslog_get(payload=None):
    url = "integrations/syslog/get"

    payload = {}
    response = jrequest.post(url, payload)
    return response

def get_user_group(payload=None):
    url = "rbac/get_user_group"

    payload = {}
    response = jrequest.post(url, payload)
    return response

def get_users(payload=None):
    url = "rbac/get_users"

    payload = {}
    response = jrequest.post(url, payload)
    return response

def policy_search(payload=None):
    url = "policy/search"
    payload = {
        "filter": {
            "AND": [
                # {
                #     "SEARCH_FIELD": "id",
                #     "SEARCH_TYPE": "CONTAINS",
                #     "SEARCH_VALUE": "b2b1279e-8760-44a8-8dca-bcc4508f8ce7",
                # },
                # {
                #     "SEARCH_FIELD": "name",
                #     "SEARCH_TYPE": "CONTAINS",
                #     "SEARCH_VALUE": "Cloud Posture Security",
                # },
            ]
        },
        "search_from": 0,
        "search_to": 500,
        "sort": [{"FIELD": "name", "ORDER": "ASC"}],
    } # This works as-is 3/26/2026
    response = jrequest.post(url, payload)
    return response

def iam_user():
    url = "platform/iam/v1/user"
    # url = f"{domain}/public_api/v1/platform/iam/v1/user" # Intuitions
    # url = f"{domain}/platform/iam/v1/user" # Documentated 

    response = jrequest.get(url)
    return response